FROM python:3.12

WORKDIR /ml_app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY model /ml_app/model

COPY model/data /ml_app/model/data
