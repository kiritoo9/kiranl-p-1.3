from typing import List
import utils.logs as logs

from engines.dtos.pruning import Pruning as pruning_model

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

class Nlsql:
    LINE_SPARE: int = 100

    serialized_words: List[str] = []
    ctx: pruning_model

    def run(self, prompt: str):
        logs.write("info", "NLSQL is running..")

        try:
            self.serialization(prompt)
            self.pruning()
        except Exception as e:
            logs.write("error", f"Something went wrong: {str(e)}")


    def serialization(self, prompt: str) -> str:
        logs.write("info", "Start to serializing user prompt..")
        
        from engines.libs.serialization import Serialization
        fn_ser = Serialization(prompt)
        self.serialized_words = fn_ser.segmented_prompt

        # show logs
        logs.write("info", "Serializing prompt completed!")
        print("-" * self.LINE_SPARE)


    def pruning(self):
        logs.write("info", "Start pruning context..")

        from engines.libs.pruning import Pruning
        fn_pru = Pruning(model, self.serialized_words)
        self.ctx = fn_pru.output
        if self.ctx.table_name is None or self.ctx.table_name == "":
            raise ValueError("no-context found!")

        print(self.ctx)
        logs.write("info", "Pruning context completed!")
        print("-" * self.LINE_SPARE)


    def rag(self):
        pass


    def query(self):
        pass


    def finalization(self):
        output = {
            "rows": [...],
            "report_type": "bar_chart",
            "value_type": "multi_value",
            "axis": {
                "x": "xfield",
            },
            "backend": {
                "endpoints": "https://api.nlp/ctx/xys-sjs-sss",
                "parameters": {
                    "page": 1,
                    "total_page": 10,
                    "size": 10,
                },
                "filters": [
                    {
                        "label": "Tgl. Pembayaran",
                        "value": "tgl_pembayaran",
                        "type": "date"
                    }, {
                        "label": "Status",
                        "value": "status",
                        "type": "option",
                        "choices": [
                            {
                                "label": "OptionA",
                                "value": "option-a"
                            }
                        ]
                    }, {
                        "label": "Customer Name",
                        "value": "customer_name",
                        "type": "text",
                    }
                ]
            }
        }