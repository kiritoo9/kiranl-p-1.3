import os
import math
import json
import utils.logs as logs

from typing import List
from datetime import datetime
from engines.nlsql import Nlsql
from config.db.conn import db_conn
from utils.format import validate_output

class Handler:
    cls_nlsql = Nlsql()

    def nl2sql(self, prompt: str):
        response = self.cls_nlsql.run(prompt)

        if response.get("data").get("rows") is not None:
            rows = validate_output(response.get("data").get("rows"))
            response["data"]["rows"] = rows

        return response
    

    def _execute_query(self, query):
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
            

    def change_context(self, body):
        # check history by ctx-id
        file_path = "./history/{}.json".format(body.get("id"))

        if os.path.exists(file_path):
            content = None
            with open(file_path, "r") as f:
                content = json.loads(f.read())

            if content is None:
                raise

            # generate base query by content
            rows_query = "SELECT {} FROM {} WHERE {}"
            count_query = "SELECT COUNT(1) FROM {} WHERE {}"

            # translate query condition
            where: List[str] = []
            where.append("deleted = false")

            if body.get("filters") is not None and len(body.get("filters")) > 0:
                for f in body.get("filters"):
                    name = f.get("name")
                    op = f.get("operator").upper()
                    val = f.get("value")

                    if op == "BETWEEN" and isinstance(val, (list, tuple)) and len(val) >= 2:
                        where.append(f"{name} BETWEEN '{val[0]}' AND '{val[1]}'")
                    else:
                        if isinstance(val, str):
                            where.append(f"{name} {op} '{str(val)}'")
                        elif isinstance(val, int):
                            where.append(f"{name} {op} {int(val)}")

            # apppending value for query
            rows_query = rows_query.format(
                ",".join(content.get("columns")) if content.get("columns") is not None and len(content.get("columns")) > 0 else "*",
                content.get("table_name"),
                " AND ".join(where)
            )

            count_query = count_query.format(
                content.get("table_name"),
                " AND ".join(where)
            )

            if body.get("order_by") is not None and body.get("order_by") != "":
                rows_query += " ORDER BY {}".format(body.get("order_by"))

            page = int(body.get("page")) if body.get("page") is not None and int(body.get("page")) > 0 else 1
            size = int(body.get("size")) if body.get("size") is not None and int(body.get("size")) > 0 else 10
            if page > 0 and size > 0:
                offset = (page * size) - size
                rows_query += f" LIMIT {size} OFFSET {offset} "

            # executing query
            try:
                rows = self._execute_query(rows_query)
                count = self._execute_query(count_query)
                if count is not None and len(count) > 0:
                    count = count[0].get("count") if count[0].get("count") is not None else 0

                # prepare for output
                total_page: int = 1
                if size > 0 and count > 0:
                    total_page = math.ceil(count / size)
                    
                output = {
                    "rows": validate_output(rows),
                    "parameters": {
                        "page": page,
                        "total_page": total_page,
                        "size": size,
                    },
                }
                
                # write in history
                if content.get("query_history") is not None:
                    content.get("query_history").append({
                        str(datetime.now()): [rows_query, count_query]
                    })

                    with open(file_path, "w") as f:
                        f.write(json.dumps(content, indent=4))

                # send response
                return output
            except Exception as e:
                raise e
        else:
            raise ValueError("data-log is missing or expired")