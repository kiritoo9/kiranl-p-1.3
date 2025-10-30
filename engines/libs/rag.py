import json
from groq import Groq

from config.env.env import Env
from engines.dtos.rag import RagSchema
from engines.dtos.pruning import Pruning as pruning_model

class RAG:
    SOURCE_PROMPT: str = "sources/prompts"
    env = Env()

    def __init__(self, prompt: str, ctx: pruning_model):
        self.prompt = prompt
        self.generated_prompt = None
        self.ctx = ctx
        self.rag_output: RagSchema


    def run_rag(self):
        prompt_text = ""
        with open(f"{self.SOURCE_PROMPT}/base_prompt.md", "r") as p:
            prompt_text = p.read()

            prompt_text = prompt_text.replace("__USER_PROMPT__", self.prompt)
            prompt_text = prompt_text.replace("__TABLE_SCHEMA__", self.ctx.table_schema)
        
        if prompt_text == "":
            raise ValueError("Prompt is empty!")
        
        self.generated_prompt = prompt_text

        # call llm (groq)
        self.groq_llm()


    def groq_llm(self):
        client = Groq(api_key=self.env.GROQ_API_KEY)

        completion = client.chat.completions.create(
            model=self.env.GROQ_LLM,
            messages=[
                {
                    "role": "user",
                    "content": self.generated_prompt
                }
            ],
            temperature=0.3,
            max_completion_tokens=300,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None
        )

        # get value response
        g_resp = completion.choices[0].message
        content_str = g_resp.content
        content_data = json.loads(content_str)
        content_dict: RagSchema = RagSchema(**content_data)

        # validate valid data
        if not getattr(content_dict, "filters", None):
            raise ValueError("Cannot connect to LLM")

        if getattr(content_dict, "greeting_statements", None) and len(getattr(content_dict, "filters", [])) == 0:
            raise ValueError(content_dict.greeting_statements)

        self.rag_output = content_dict
