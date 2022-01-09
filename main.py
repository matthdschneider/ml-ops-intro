from typing import List
from fastapi import FastAPI
from flair.models import TextClassifier
from flair.data import Sentence
from pydantic import BaseModel
import spacy
import json

class Sentences(BaseModel):
    sentences: List[str]

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    classifier = TextClassifier.load('en-sentiment')
    return classifier

@app.get("/")
async def root():
    return {"message": "Hello HSRW"}


@app.post("/sentiment/")
async def sentiment(sentences: Sentences):
    classifier = TextClassifier.load('en-sentiment')
    labels = []
    for example in sentences.sentences:
        s = Sentence(example)
        sentiment = classifier.predict(s)
        labels.append(s.labels)
    return labels


@app.post("/ner/")
async def ner(sentences: Sentences):
    new_nlp = spacy.load('model-best')
    labels = {"token": [], "ent": []}
    for sentence in sentences.sentences:
        doc = new_nlp(sentence)
        for token in doc:
            labels["token"].append(token.text)
            labels["ent"].append(token.ent_type_)
    return labels

