FROM python:3.9.18-slim-bookworm AS sentiment_analyzer


WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
RUN ls
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
