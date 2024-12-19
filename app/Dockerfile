FROM python:3.10
#WORKDIR /app
#ENV PYTHONPATH="${PYTHONPATH}:/app"

COPY requirements.txt .

#WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .


CMD [ "uvicorn", "main:api", "--host", "0.0.0.0" , "--port", "8031"]
