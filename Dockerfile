FROM python:3.12

WORKDIR /ml_app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

COPY tests/ app/tests/

#CMD [ "python", "app.py" ]