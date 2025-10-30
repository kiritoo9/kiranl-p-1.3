from typing import List
import utils.logs as logs

from engines.dtos.pruning import Pruning as PruningSchema
from engines.dtos.rag import RagSchema

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

class Nlsql:
    LINE_SPARE: int = 100

    corrected_words: str
    serialized_words: List[str] = []
    ctx: PruningSchema
    rag_output: RagSchema
    data_output: dict

    def run(self, prompt: str):
        logs.write("info", "NLSQL is running..")

        try:
            self.serialization(prompt)
            self.pruning()
            self.rag()
            self.query()

            return self.data_output
        except Exception as e:
            logs.write("error", f"Something went wrong: {str(e)}")
            raise ValueError(e)


    def serialization(self, prompt: str) -> str:
        logs.write("info", "Start to serializing user prompt..")
        
        from engines.libs.serialization import Serialization
        fn_ser = Serialization(prompt)

        self.corrected_words = fn_ser.prompt
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

        logs.write("info", "Pruning context completed!")
        print("-" * self.LINE_SPARE)


    def rag(self):
        logs.write("info", "Start reasoning process..")

        # from engines.libs.rag import RAG
        # rag = RAG(self.corrected_words, self.ctx)
        # rag.run_rag()

        # get output
        logs.write("info", "RAG process is success!")
        # self.rag_output = rag.rag_output

        self.rag_output = RagSchema(
            greeting_statements='Saya dengan senang hati membantu Anda dengan permintaan tersebut.', 
            closing_statements='Terima kasih atas kepercayaan Anda, saya berharap informasi ini membantu.', 
            filters=[{'field': 'periode_rekening', 'value': '%2022%', 'operator': 'LIKE'}]
        )


    def query(self):
        logs.write("info", "Start generating query based on context..")

        from engines.libs.query import Query
        q = Query(self.ctx, self.rag_output)
        q.generate_query()

        if q.DATA_OUTPUT is None:
            raise ValueError("error while translating query")
        
        self.data_output = q.DATA_OUTPUT