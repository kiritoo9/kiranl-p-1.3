import json
import joblib
import numpy as np
import utils.logs as logs

from typing import List
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class Sim:
    TRESHOLD: float = 0.8
    L2NORM_SOURCE: str = "storages/l2norm"
    L2NORM_KEY: List[str] = ["attr", "keyword", "number", "status", "time"]

    def __init__(self):
        self.prompt = "tampilkan list tagihan air yang belum lunas pada tahun 2024"


    def increasing_chunks(self, min_word: int = 2, max_word: int = 4):
        chunks = []
        tokens = self.prompt.split()
        token_len = len(tokens)

        for size in range(min_word, max_word + 1):
            for start_idx in range(token_len - size + 1):
                end_idx = start_idx + size

                chunk = " ".join(tokens[start_idx:end_idx])
                chunks.append(chunk)

        return chunks
    

    def dot_analyzing(self, key: str, chunks: List[str]):
        # loading resources
        vectorizer = joblib.load(f"{self.L2NORM_SOURCE}/{key}/tfidf.joblib")
        normalized = np.load(f"{self.L2NORM_SOURCE}/{key}/normalized.npy")
        canonical = np.load(f"{self.L2NORM_SOURCE}/{key}/conanical.npy", allow_pickle=True)

        output: dict = {}
        for c in chunks:
            # normalize user chunk prompt
            query_vec = vectorizer.transform([c]).toarray()
            norm_query = normalize(query_vec, norm="l2", axis=1)

            # calculating dot-product
            scores = linear_kernel(norm_query, normalized)[0]
            sort_indicies = np.argsort(-scores)

            # appending value
            for i in sort_indicies:
                if scores[i] >= self.TRESHOLD:
                    if output.get(canonical[i]) is not None and output.get(canonical[i]) > scores[i]:
                        continue
                    output[canonical[i]] = scores[i]

        if not output:
            return None
        
        highest_key = max(output, key=output.get)
        return {highest_key: output[highest_key]}
    

    def run(self):
        logs.write("info", f"executing prompt: {self.prompt}")

        try:
            # splitting prompts
            chunks = self.increasing_chunks(2, 4)

            # detecting for all keys
            for k in self.L2NORM_KEY:
                output = self.dot_analyzing(k, chunks)
                logs.write("info", f"output analyzing dot for key: {k}, {output}")
            
        except Exception as e:
            logs.write("error", f"error while analyzing phrase: {str(e)}")

            