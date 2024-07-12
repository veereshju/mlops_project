FROM python:3.12

WORKDIR /ml_app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY app/model /ml_app/model

COPY app/model/data /ml_app/model/data

CMD ["python", "model_server.py"]