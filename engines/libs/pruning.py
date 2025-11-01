import numpy as np
from typing import List
import utils.logs as logs

from engines.libs.convertion import Convertion
from engines.dtos.pruning import Pruning as pruning_model
from engines.dtos.emb import Emb as emb_model

class Pruning:
    SOURCE_PATH: str = "storages"

    output: pruning_model
    convertion = Convertion()

    def __init__(self, model, words: List[str] = []):
        self.model = model
        self.words = words
        self.output: pruning_model = pruning_model(
            report_type=None,
            value_type=None,
            table_name=None,
            table_schema=None,
            column_predictions=[],
            column_schemas=[]
        )

        # perform to run pruning process
        self.report_detection()
        # self.value_detection()
        self.table_detection()
        self.column_prediction()


    def report_detection(self):
        logs.write("info", "Detecting report type..")

        # load .npy files 
        # find nearest by keywords
        emb = np.load(f"{self.SOURCE_PATH}/report_type/embeddings.npy")
        keypoints = np.load(f"{self.SOURCE_PATH}/report_type/keypoints.npy")
        res: List[emb_model] = self.convertion.find_nearest(self.model, emb, keypoints, self.words)

        # set value with default
        self.output.report_type = str(keypoints[0]) if len(res) <= 0 else res[0].value

        # write logs
        logs.write(
            "info", 
            f"Report type detected as {self.output.report_type}" 
            if res is not None 
            else "Report type not detected, set to table as default of report type!"
        )


    def value_detection(self):
        logs.write("info", "Detecting value type..")

        # load .npy files 
        # find nearest by keywords
        emb = np.load(f"{self.SOURCE_PATH}/value_type/embeddings.npy")
        keypoints = np.load(f"{self.SOURCE_PATH}/value_type/keypoints.npy")
        res: List[emb_model] = self.convertion.find_nearest(self.model, emb, keypoints, self.words)

        # set value with default
        self.output.value_type = str(keypoints[0]) if len(res) <= 0 else res[0].value

        # write logs
        logs.write(
            "info", 
            "Value type detected!" 
            if res is not None 
            else "Value type not detected, set to single_value as default of value type!"
        )


    def table_detection(self):
        logs.write("info", "Detecting table name..")

        # load .npy files 
        # find nearest by keywords
        emb = np.load(f"{self.SOURCE_PATH}/main_table/embeddings.npy")
        keypoints = np.load(f"{self.SOURCE_PATH}/main_table/keypoints.npy")
        res: List[emb_model] = self.convertion.find_nearest(self.model, emb, keypoints, self.words)

        # set value
        if len(res) > 0:
            self.output.table_name = res[0].value

            # load table schema
            schemas = np.load(f"{self.SOURCE_PATH}/table_schemas/{self.output.table_name}/schemas.npy")
            table_schema: str = ""
            for s in schemas:
                s = s.split("; ")
                dt = s[2].split("=")[1]

                schema = f"{s[0]} ({dt}), {s[4]}"

                table_schema += f"{schema}\n"
            self.output.table_schema = table_schema

            logs.write("info", "Table name detected!")
        else:
            logs.write("info", "Table name not detected, user might be ask out of context!")


    def column_prediction(self):
        if self.output.table_name is None or self.output.table_name == "":
            return

        logs.write("info", f"Detecting column based on table: {self.output.table_name}..")

        # load .npy files 
        # find nearest by keywords
        emb = np.load(f"{self.SOURCE_PATH}/table_schemas/{self.output.table_name}/embeddings.npy")
        indexes = np.load(f"{self.SOURCE_PATH}/table_schemas/{self.output.table_name}/indexes.npy")
        schemas = np.load(f"{self.SOURCE_PATH}/table_schemas/{self.output.table_name}/schemas.npy")
        keypoints = np.load(f"{self.SOURCE_PATH}/table_schemas/{self.output.table_name}/keypoints.npy")
        res: List[emb_model] = self.convertion.find_nearest(self.model, emb, keypoints, self.words, treshold=0.95)

        # set value
        for r in res:
            if r.value not in self.output.column_predictions:
                self.output.column_predictions.append(r.value)
                self.output.column_schemas.append(schemas[indexes[r.index]])

        if len(res) > 0:
            logs.write("info", f"Found {len(self.output.column_predictions)} columns to select!")
        else:
            logs.write("info", f"No specific column to select, registering entire columns")

            for s in schemas:
                self.output.column_schemas.append(s)