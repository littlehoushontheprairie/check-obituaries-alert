import os
import logging
import schedule
import time
from smtp import SMTP
from email_templates import EmailTemplates
from legacy_com_api import LegacyComApi, LegacyComApiError, LegacyComApiMissingParameterError

FROM_EMAIL = os.environ.get('FROM_EMAIL')
TO_EMAIL = os.environ.get('TO_EMAIL')
EMAIL_GREETING = os.environ.get('EMAIL_GREETING')
SMTP_URL = os.environ.get('SMTP_URL')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_EMAIL = os.environ.get('SMTP_EMAIL')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

# Enable logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


def job():
    logging.info('Running job...')
    smtp = SMTP(smtp_url=SMTP_URL, smtp_port=SMTP_PORT,
                smtp_email=SMTP_EMAIL, smtp_password=SMTP_PASSWORD)
    email_templates = EmailTemplates()
    legacyComApi = LegacyComApi()

    try:
        obituaries = legacyComApi.call()

        if len(obituaries) == 0:
            logging.info("No new obituaries were found.")
        else:
            subject = "{} obituaries have been found.".format(
                str(len(obituaries)))
            body = email_templates.generate_basic_template(
                dict(email_greeting=EMAIL_GREETING, obituaries=email_templates.generate_obituaries_body(
                    obituaries)))
            smtp.send_email(from_email=FROM_EMAIL,
                            to_email=TO_EMAIL, subject=subject, body=body)
            logging.info(subject)

    except LegacyComApiError as error:
        subject = "check-obituaries.py encountered an error from Legacy.com"
        body = email_templates.generate_error_template(
            dict(email_greeting=EMAIL_GREETING, status_code=error.args[1]))
        smtp.send_email(from_email=FROM_EMAIL, to_email=TO_EMAIL,
                        subject=subject, body=body)
        logging.error(
            "An error has occurred when making Legacy.com api call. API returned status code: {}".format(error.args[1]))
    except LegacyComApiMissingParameterError as error:
        logging.error("Legacy.com API requires a first name or last name.")

    logging.info('Job finished.')


# schedule.every().day.at("15:00").do(job)
schedule.every(30).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
