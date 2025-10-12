import json
import numpy as np
import Levenshtein
from typing import List

from engines.dtos.emb import Emb as emb_model

class Convertion:
    TOP_K: int = 2
    TRESHOLD: int = 0.9

    def train_datasets(self, model, source: str, target: str, keypoint: str):
        with open(source, "r") as rt:
            data = [json.loads(v) for v in rt if v.strip()]

            keywords = []
            indexes = []
            schemas = []
            _keypoints = []

            for i, v in enumerate(data):
                if keypoint.lower() == "column_name":
                    if v.get("exclude") is True:
                        continue

                    _schema: str = "column_name={}; index={}; data_type={}; description={}; example_value={}".format(
                        v.get("column_name"),
                        v.get("index"),
                        v.get("data_type"),
                        v.get("description"),
                        v.get("example_value"),
                    )
                    schemas.append(_schema)
                
                keywords.extend(v.get("keywords"))
                indexes.extend([i] * len(v.get("keywords")))
                _keypoints.extend([v.get(keypoint)] * len(v.get("keywords")))

            # new-embed or replace
            embeddings = model.encode(np.array(keywords).tolist(), convert_to_numpy=True)
            np.save(f"{target}/embeddings.npy", embeddings)
            np.save(f"{target}/indexes.npy", np.array(indexes))
            np.save(f"{target}/keypoints.npy", np.array(_keypoints))
            if len(schemas) > 0:
                np.save(f"{target}/schemas.npy", np.array(schemas))


    def find_nearest(self, model, emb, keypoints, words: List[str] = [], treshold: float = 0.0) -> List[emb_model]:
        treshold = treshold if treshold > 0 else self.TRESHOLD
        emb = emb / np.linalg.norm(emb, axis=1, keepdims=True) # normalize embedding to cosine standard

        res: List[emb_model] = []
        for w in words:
            vec = model.encode([w], convert_to_numpy=True)
            vec = vec / np.linalg.norm(vec, axis=1, keepdims=True)

            cos_sim = np.dot(emb, vec.T).ravel()
            idx = np.argsort(-cos_sim)[:self.TOP_K]

            for i in idx:
                if cos_sim[i] >= treshold:
                    res.append(emb_model(
                        score=cos_sim[i],
                        index=int(i),
                        value=str(keypoints[i])
                    ))

        return res


    def levensthein(self, word: str, abbreviation: dict, id_words: List[str], en_words: List[str]) -> str:
        word = word.lower().strip()

        # check abbreviation
        if abbreviation.get(word) is not None:
            return abbreviation.get(word)

        # check if words already valid in id_words
        if word in id_words:
            return word
        
        # perform to add formulas
        max_distance: int = 2
        min_ratio: float = 0.6
        def _lev(word: str, dictionary: List[str]):
            candidates = []
            for w in dictionary:
                dist = Levenshtein.distance(word, w)
                ratio = Levenshtein.ratio(word, w)

                if dist <= max_distance or ratio >= min_ratio:
                    candidates.append((w, dist, ratio))
            return candidates

        
        # check multilingual words
        id_check = _lev(word, id_words)
        if id_check:
            return max(id_check, key=lambda x: x[2])[0]
        
        en_check = _lev(word, en_words)
        if en_check:
            return max(en_check, key=lambda x: x[2])[0]
        
        return word