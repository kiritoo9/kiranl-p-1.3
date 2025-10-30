import os
from engines.nlsql import Nlsql

class Handler:
    cls_nlsql = Nlsql()

    def nl2sql(self, prompt: str):
        response = self.cls_nlsql.run(prompt)

        return response
    

    def change_context(self, body):
        # check history by ctx-id
        file_path = "./history/{}.json".format(body.get("id"))

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()

                print(content)

                # generate filter
                if body.get("filter") is not None:
                    pass

                # executing query

                # write in history
        else:
            raise ValueError("data-log is missing or expired")