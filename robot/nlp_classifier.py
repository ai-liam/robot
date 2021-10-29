#!/usr/bin/python3
# -*- coding: utf-8 -*-

from transformers import pipeline
from transformers import AutoModelForSequenceClassification,AutoTokenizer

# https://huggingface.co/uer/roberta-base-finetuned-chinanews-chinese
_model_dir = '/Users/liampro/Downloads/dataLake/Models/nlp/huggingface/uer/roberta-base-finetuned-chinanews-chinese'

class NLPClassifier:
    def __init__(self,model_dir=_model_dir,text_type='sentiment-analysis'):
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        self.text_classification = pipeline(text_type, model=model, tokenizer=tokenizer)

    def predict(self,text):
        return self.text_classification(text)