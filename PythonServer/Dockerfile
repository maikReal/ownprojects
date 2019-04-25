FROM python:latest
ADD . /code
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "server.py"]
