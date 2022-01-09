from typing import List
from fastapi import FastAPI
from flair.models import TextClassifier
from flair.data import Sentence
from pydantic import BaseModel
#import json

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
    for example in sentences.sentences:
        s = Sentence(example)
        sentiment = classifier.predict(s)
    return s.labels
