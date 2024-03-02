FROM python:latest

WORKDIR /usr/src/app

COPY check_obituaries_alert.py .
COPY legacy_com_api.py .
COPY smtp.py .
COPY email_templates.py .
COPY templates/index.html ./templates/index.html
COPY templates/error.html ./templates/error.html
RUN chmod 0755 check_obituaries_alert.py legacy_com_api.py smtp.py email_templates.py templates/index.html templates/error.html 
RUN pip install requests schedule

CMD [ "python", "./check_obituaries_alert.py" ]
