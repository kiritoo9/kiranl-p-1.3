from engines.dtos.pruning import Pruning as pruning_model

class RAG:
    SOURCE_PROMPT: str = "sources/prompts"

    def __init__(self, prompt: str, ctx: pruning_model):
        self.prompt = prompt
        self.ctx = ctx


    def rag_query(self):
        prompt_text = ""
        with open(f"{self.SOURCE_PROMPT}/base_prompt.md", "r") as p:
            prompt_text = p.read()

            prompt_text = prompt_text.replace("__USER_PROMPT__", self.prompt)
            prompt_text = prompt_text.replace("__TABLE_SCHEMA__", self.ctx.table_schema)
        
        if prompt_text == "":
            raise ValueError("Prompt is empty!")
        
        print(prompt_text)