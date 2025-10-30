import os
import uuid
import json
import math
from datetime import datetime
import utils.logs as logs

from typing import List
from config.db.conn import db_conn
from engines.dtos.pruning import Pruning as PruningSchema
from engines.dtos.rag import RagSchema

class Query:
    MAX_DATA_LIMIT: int = 50
    DATA_LIMIT: int = 10

    QUERY_ROWS: str
    QUERY_COUNT: str

    DATA_OUTPUT: dict | None = None

    def __init__(self, ctx: PruningSchema, rag: RagSchema):
        self.ctx = ctx
        self.rag = rag
        self.output = None


    def generate_query(self):
        # define base variable
        columns = self.ctx.column_predictions
        filters = self.rag.filters

        where_str: List[str] = []
        order_by: List[str] = []

        # default where condition [special case]
        where_str.append("deleted = false")

        for f in filters:
            op = f.get("operator").upper()
            field = f.get("field")
            val = f.get("value")

            if op is None or field is None or val is None:
                continue

            if op.upper() == "ORDER_BY":
                order_by.append(f"{field} {val}")
            elif op.upper() == "LIMIT":
                self.DATA_LIMIT = int(val)
                if self.DATA_LIMIT > self.MAX_DATA_LIMIT:
                    self.DATA_LIMIT = self.MAX_DATA_LIMIT
            else:
                # where condition here
                if op.upper() == "BETWEEN":
                    if val is not None and isinstance(val, (list, tuple)) and len(val) >= 2:
                        where_str.append(f" BETWEEN {val[0]} AND {val[1]} ")
                else:
                    val = f"'{val}'" if isinstance(val, str) else val
                    where_str.append(f" {field} {op} {val} ")

        # translating query
        self.QUERY_ROWS = "SELECT {} FROM {} WHERE {}".format(
            ",".join(columns) if len(columns) > 0 else "*",
            self.ctx.table_name,
            " AND ".join(where_str)
        )

        if len(order_by) > 0:
            self.QUERY_ROWS += " ORDER BY {}".format(", ".join(order_by))

        if self.DATA_LIMIT is not None and self.DATA_LIMIT > 0:
            self.QUERY_ROWS += f" LIMIT {self.DATA_LIMIT} OFFSET 0"

        self.QUERY_COUNT = "SELECT COUNT(1) FROM {} WHERE {}".format(
            self.ctx.table_name,
            " AND ".join(where_str)
        )

        # start executing query
        rows = self.execute_query(self.QUERY_ROWS)
        count = self.execute_query(self.QUERY_COUNT)
        if len(count) > 0:
            count = count[0].get("count") if count[0].get("count") is not None else 0

        self.finalize_output(rows, count)


    def execute_query(self, query: str):
        try:
            logs.write("info", f"Executing query: {query}")
            with db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    columns = [desc[0] for desc in cur.description]
                    response = cur.fetchall()

                    rows = []
                    for v in response:
                        col = {}
                        for k, j in enumerate(v):
                            col[columns[k]] = j
                        rows.append(col)

                    return rows
        except Exception as e:
            raise e


    def finalize_output(self, rows, count: int = 0):
        # calculating total page
        total_page: int = 1
        if self.DATA_LIMIT > 0 and count > 0:
            total_page = math.ceil(count / self.DATA_LIMIT)

        # define filters based on column selected
        def _get_schema_value(val: str):
            val = val.split("=")
            if len(val) <= 0:
                return None
            return val[1]


        col_schemas = self.ctx.column_schemas
        filters = []
        for col in col_schemas:
            col = col.split(";")
            if len(col) <= 2:
                continue

            col_name = _get_schema_value(col[0])
            col_type = _get_schema_value(col[2])

            if col_name is not None and col_type is not None:
                filters.append({
                    "name": col_name,
                    "type": col_type
                })

        # store attributes for dynamic report
        now = datetime.now()
        prompt_id = str(uuid.uuid4())

        base_path = f"./history"
        os.makedirs(base_path, exist_ok=True)
        file_name = f"{prompt_id}.json"
        file_path = os.path.join(base_path, file_name)

        with open(file_path, "w") as w:
            w.write(json.dumps({
                "table_name": self.ctx.table_name,
                "columns": self.ctx.column_predictions,
                "query_history": [{str(now): [self.QUERY_ROWS, self.QUERY_COUNT]}]
            }, indent=4))

        # prepare for output
        self.DATA_OUTPUT = {
            "sentences": {
                "greeting": self.rag.greeting_statements,
                "closing": self.rag.closing_statements,
            },
            "report_type": self.ctx.report_type,
            "value_type": self.ctx.value_type,
            "data": {
                "id": prompt_id,
                "rows": rows,
                "parameters": {
                    "page": 1,
                    "total_page": total_page,
                    "size": self.DATA_LIMIT,
                },
                "filters": filters
            }
        }