import os
import logging
import schedule
import time
from smtp import SMTP
from email_templates import EmailTemplates
from legacy_com_api import LegacyComApi, LegacyComApiError, LegacyComApiMissingParameterError

SCRIPT_RUN_TIME: str = os.environ.get("SCRIPT_RUN_TIME", "13:00")
FROM_EMAIL: str = os.environ.get("FROM_EMAIL", "")
TO_EMAIL: str = os.environ.get("TO_EMAIL", "")
EMAIL_GREETING: str = os.environ.get("EMAIL_GREETING", "")
SMTP_URL: str = os.environ.get("SMTP_URL", "")
SMTP_PORT: str = os.environ.get("SMTP_PORT", "")
SMTP_EMAIL: str = os.environ.get("SMTP_EMAIL", "")
SMTP_PASSWORD: str = os.environ.get("SMTP_PASSWORD", "")

# Enable logging
logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s",
                    level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")


def job():
    logging.info("Running job...")
    smtp: SMTP = SMTP(smtp_url=SMTP_URL, smtp_port=SMTP_PORT,
                      smtp_email=SMTP_EMAIL, smtp_password=SMTP_PASSWORD)
    email_templates: EmailTemplates = EmailTemplates()
    legacyComApi: LegacyComApi = LegacyComApi()

    try:
        if len(legacyComApi.obituaries) == 0:
            logging.info("No new obituaries were found.")
        else:
            subject: str = "{} obituaries have been found.".format(
                str(len(legacyComApi.obituaries)))
            body: str = email_templates.generate_basic_template(
                dict(email_greeting=EMAIL_GREETING, obituaries=email_templates.generate_obituaries_body(
                    legacyComApi.obituaries)))
            smtp.send_email(from_email=FROM_EMAIL,
                            to_email=TO_EMAIL, subject=subject, body=body)
            logging.info(subject)

    except LegacyComApiError as error:
        subject: str = "check-obituaries.py encountered an error from Legacy.com"
        body: str = email_templates.generate_error_template(
            dict(email_greeting=EMAIL_GREETING, status_code=error.args[1]))
        smtp.send_email(from_email=FROM_EMAIL, to_email=TO_EMAIL,
                        subject=subject, body=body)
        logging.error(
            "An error has occurred when making Legacy.com api call. API returned status code: {}".format(error.args[1]))
    except LegacyComApiMissingParameterError as error:
        logging.error("Legacy.com API requires a first name or last name.")

    logging.info("Job finished.")


schedule.every().day.at(SCRIPT_RUN_TIME).do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
