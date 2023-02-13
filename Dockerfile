FROM python:3

WORKDIR /usr/src/app

COPY check-obituaries.py .
RUN chmod 0755 check-obituaries.py
RUN pip install requests schedule

CMD [ "python", "./check-obituaries.py" ]