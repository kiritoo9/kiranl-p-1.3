import os
import json
import pickle
import utils.logs as logs

from wordfreq import top_n_list
from sentence_transformers import SentenceTransformer
from engines.libs.convertion import Convertion

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

class Training:
    SOURCE_DIR: str = "./sources/datasets"
    TARGET_DIR: str = "./storages"

    TOP_N: int = 32000
    MODEL = model

    convertion = Convertion()

    def run(self):
        logs.write("info", "Training start..")

        try:
            self.abbreviation()
            self.dictionary()
            self.report_type()
            self.value_type()
            self.main_tables()
            self.columns()

            logs.write("info", "Training data completed!")
        except Exception as e:
            logs.write("error", f"Something went wrong: {str(e)}")


    def abbreviation(self):
        logs.write("info", "Generating abbreviation..")

        abbrv = []
        with open(f"{self.SOURCE_DIR}/abbreviation.jsonl", "rb") as a:
            abbrv = [json.loads(v) for v in a]

        with open(f"{self.TARGET_DIR}/abbreviation.pkl", "wb") as d:
            pickle.dump({item.get("val1") : item.get("val2") for item in abbrv}, d)

        logs.write("info", "Abbreviation generated!")


    def dictionary(self):
        logs.write("info", "Generating dictionary..")
        data = {    
            "en": set(top_n_list("en", self.TOP_N)),
            "id": set(top_n_list("id", self.TOP_N))
        }
        with open(f"{self.TARGET_DIR}/dictionary.pkl", "wb") as d:
            pickle.dump(data, d)

        logs.write("info", "Dictionary generated!")


    def report_type(self):
        logs.write("info", "Vectoring report types..")
        
        # embedding datasets and store as .npy
        source = f"{self.SOURCE_DIR}/report_type.jsonl"
        target = f"{self.TARGET_DIR}/report_type"
        self.convertion.train_datasets(self.MODEL, source, target, "type")

        logs.write("info", "Report types embedding generated!")


    def value_type(self):
        logs.write("info", "Vectoring value types..")
        
        # embedding datasets and store as .npy
        source = f"{self.SOURCE_DIR}/value_type.jsonl"
        target = f"{self.TARGET_DIR}/value_type"
        self.convertion.train_datasets(self.MODEL, source, target, "type")

        logs.write("info", "Value types embedding generated!")


    def main_tables(self):
        logs.write("info", "Vectoring main tables..")
        
        # embedding datasets and store as .npy
        source = f"{self.SOURCE_DIR}/main_table.jsonl"
        target = f"{self.TARGET_DIR}/main_table"
        self.convertion.train_datasets(self.MODEL, source, target, "table")

        logs.write("info", "Main tables embedding generated!")


    def columns(self):
        logs.write("info", "Vectoring table schemas..")
        
        # embedding datasets and store as .npy
        source = f"{self.SOURCE_DIR}/tables"
        target = f"{self.TARGET_DIR}/table_schemas"

        for f in os.listdir(source):
            filename = f.split(".")[0]
            target = f"{target}/{filename}"
            os.makedirs(target, exist_ok=True)

            self.convertion.train_datasets(self.MODEL, f"{source}/{f}", target, "column_name")

        logs.write("info", "All table schemas successfully embeedded")