from fastapi import FastAPI
import spacy
from pydantic import BaseModel
from typing import List
from flair.models import TextClassifier
from flair.data import Sentence


class Sentences(BaseModel):
    sentences: List[str]

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    classifier = TextClassifier.load('en-sentiment')
    return classifier


@app.get("/")
async def root():
    return {"message": "Hello everyone, I am super happy this works."}


@app.post("/sentiment/")
async def sentiment(text: Sentences):
    # classifier = TextClassifier.load('en-sentiment')
    labels = []
    for sentence in text.sentences:
        s = Sentence(sentence)
        sentiment = classifier.predict(s)
        labels.append(s.labels)
    return labels


@app.post("/ner/")
async def ner(text: Sentences):
    new_nlp = spacy.load("model-best")
    labels = []
    for sentence in text.sentences:
        doc = new_nlp(sentence)
        for token in doc:
            labels.append(token.ent_type_)
    return labels