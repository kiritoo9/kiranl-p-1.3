import os
import re
import pickle

import utils.logs as logs
from typing import List

class Serialization:
    ABBREVIATION_PATH: str = "storages/abbreviation.pkl"
    DICTIONARY_PATH: str = "storages/dictionary.pkl"

    prompt: str
    segmented_prompt: List[str] = []
    id_words: any = None
    en_words: any = None

    def __init__(self, prompt: str):
        self.prompt = prompt

        try:
            self.normalization()
            self.typo_correction()
            self.segmentation()
        except Exception as e:
            raise e 

    def normalization(self):
        logs.write("info", "Normalization process..")
    
        p = self.prompt
        p = p.lower().strip()

        # regex function
        _normalize_re = re.compile(r"[^a-zA-Z0-9\s]", re.UNICODE)
        p = _normalize_re.sub("", p)
        p = re.sub(r"\s+", " ", p)
        self.prompt = p
        
        logs.write("info", "Normalization completed!")


    def typo_correction(self):
        logs.write("info", "Typo detection..")

        # load abbreviation
        if not os.path.exists(self.ABBREVIATION_PATH):
            raise ValueError("abbreviation file is not found!")
        
        with open(self.ABBREVIATION_PATH, "rb") as a:
            abbreviation = pickle.load(a)    

        # load dictionary
        if not os.path.exists(self.DICTIONARY_PATH):
            raise ValueError("dictionary file is not found!")
        
        with open(self.DICTIONARY_PATH, "rb") as d:
            dictionary = pickle.load(d)
            self.id_words = dictionary["id"]
            self.en_words = dictionary["en"]

        if self.id_words is None or self.en_words is None:
            raise ValueError("words in dictionary is empty!")

        # perform to compare words
        from engines.libs.convertion import Convertion
        conv = Convertion()

        corrected_text = []
        for w in self.prompt.split():
            corrected_text.append(conv.levensthein(w, abbreviation, self.id_words, self.en_words))

        self.prompt = " ".join(corrected_text)
        logs.write("info", f"Detection completed!\n\t\tCorrected prompt: {self.prompt}")

    def segmentation(self):
        logs.write("info", "Segmentation process..")

        # split 2 words with overlap 1
        prompt = self.prompt.split()
        for i in range(len(prompt) - 1):
            self.segmented_prompt.append(prompt[i] + " " + prompt[i + 1])

        logs.write("info", "Segementation completed!")