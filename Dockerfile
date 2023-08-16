FROM python:latest

WORKDIR /usr/src/app

COPY check_obituaries.py .
COPY smtp.py .
COPY email_templates.py .
COPY templates .
RUN chmod 0755 check_obituaries.py smtp.py email_templates.py
RUN pip install requests schedule

CMD [ "python", "./check_obituaries.py" ]
