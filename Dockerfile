FROM python:3.10
WORKDIR /app
ENV PYTHONPATH="${PYTHONPATH}:/app"

COPY ./requirements.txt /api/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /api/requirements.txt

COPY ./app .

CMD [ "python", "main.py"]