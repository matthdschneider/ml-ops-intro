FROM python:3.9.9-slim

# install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip setuptools wheel
RUN pip install -r requirements.txt

COPY . ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]