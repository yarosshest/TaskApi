FROM python:3.10
WORKDIR /app
ENV PYTHONPATH="${PYTHONPATH}:/app"

COPY ../MIREA_MicroServices/TaskApi/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY ./app .

CMD [ "python", "main.py"]