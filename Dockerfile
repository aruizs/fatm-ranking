FROM python:3.8-alpine

ENV FLASK_APP fatm.py
ENV FLASK_CONFIG production

RUN adduser -D fatm
USER fatm

WORKDIR /home/fatm

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY templates templates
COPY wsgi.py fatm.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]