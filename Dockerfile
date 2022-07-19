FROM --platform=linux/amd64 python:slim

RUN useradd flaskjwt
RUN apt-get update && apt-get install

RUN apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean


WORKDIR /home/flaskjwt

COPY setup.py setup.py
COPY run.py run.py
COPY README.md ./
COPY src src
COPY migrations migrations
COPY .env ./

RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip setuptools wheel 
RUN venv/bin/pip install gunicorn cryptography
RUN venv/bin/pip install .



COPY boot.sh ./
RUN chmod +x boot.sh

RUN chown -R flaskjwt:flaskjwt ./
USER flaskjwt

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
