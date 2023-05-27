FROM python:latest

WORKDIR /usr/src/app

COPY check-obituaries.py .
COPY tiny_jmap_library.py .
RUN chmod 0755 check-obituaries.py tiny_jmap_library.py
RUN pip install requests schedule

CMD [ "python", "./check-obituaries.py" ]
