import os
import logging
import schedule
import time
from smtp import SMTP, Email, SMTPOptions
from email_templates import EmailTemplates
from legacy_com_api import LegacyComApi, LegacyComApiError, LegacyComApiMissingParameterError

SCRIPT_RUN_TIME: str = os.environ.get("SCRIPT_RUN_TIME", "13:00")
FROM_NAME: str = os.environ.get("FROM_NAME", "Check Obituaries Alert")
FROM_EMAIL: str = os.environ.get("FROM_EMAIL", "")
TO_NAME: str = os.environ.get("TO_NAME", "")
TO_EMAIL: str = os.environ.get("TO_EMAIL", "")

SMTP_HOST: str = os.environ.get("SMTP_HOST", "")
SMTP_PORT: int = os.environ.get("SMTP_PORT", 465)
SMTP_USER: str = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD: str = os.environ.get("SMTP_PASSWORD", "")

# Enable logging
logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s",
                    level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")


def job():
    logging.info("Running job...")
    smtpOptions: SMTPOptions = SMTPOptions(
        host=SMTP_HOST, port=SMTP_PORT, username=SMTP_USER, password=SMTP_PASSWORD)
    smtp: SMTP = SMTP(smtp_options=smtpOptions)
    email_templates: EmailTemplates = EmailTemplates()
    legacyComApi: LegacyComApi = LegacyComApi()

    try:
        if len(legacyComApi.obituaries) == 0:
            logging.info("No new obituaries were found.")
        else:
            email: Email = Email(from_name=FROM_NAME, from_email=FROM_EMAIL, to_name=TO_NAME, to_email=TO_EMAIL,
                                 subject=f"{str(len(legacyComApi.obituaries))} new obituaries have been found.",
                                 body=email_templates.generate_basic_template(
                                     dict(to_name=TO_NAME, obituaries=email_templates.generate_obituaries_body(
                                         legacyComApi.obituaries))))
            smtp.send_email(email=email)
            logging.info(
                f"{str(len(legacyComApi.obituaries))} obituaries have been found.")

    except LegacyComApiError as error:
        email: Email = Email(from_name=FROM_NAME, from_email=FROM_EMAIL, to_name=TO_NAME, to_email=TO_EMAIL,
                             subject="check-obituaries.py encountered an error from Legacy.com",
                             body=email_templates.generate_error_template(
                                 dict(to_name=TO_NAME, status_code=error.args[1])))
        smtp.send_email(email=email)
        logging.error(
            f"An error has occurred when making Legacy.com api call. API returned status code: {error.args[1]}")
    except LegacyComApiMissingParameterError as error:
        logging.error("Legacy.com API requires a first name or last name.")

    logging.info("Job finished.")


# schedule.every().day.at(SCRIPT_RUN_TIME).do(job)
schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
