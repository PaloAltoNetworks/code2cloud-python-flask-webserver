FROM python:3.10

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get upgrade -y && apt-get clean

# Upgrade pip to latest version
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

# Ensure SQLite is installed
RUN apt-get install -y sqlite3

EXPOSE 5000

HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1   

CMD python ./index.py

