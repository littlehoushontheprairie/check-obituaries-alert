import os
import requests
import logging
import schedule
import time
from smtp import SMTP
from email_templates import EmailTemplates

FROM_EMAIL = os.environ.get('FROM_EMAIL')
TO_EMAIL = os.environ.get('TO_EMAIL')
EMAIL_GREETING = os.environ.get('EMAIL_GREETING')
SMTP_URL = os.environ.get('SMTP_URL')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_EMAIL = os.environ.get('SMTP_EMAIL')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

LAST_NAMES = os.environ.get('LAST_NAMES')

USER_AGENT = 'Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1'
NO_RESULTS_TEMPLATE = 'Your search for "<span style=\'color:#FD6717\'>{}</span>" did not find any obituaries in this newspaper.'

# date range 99999 - All, 1 - Today
SEARCH_URL_TEMPLATE = 'https://www.legacy.com/obituaries/rapidcity/obituary-search.aspx?daterange=1&lastname={}&countryid=1&stateid=54&affiliateid=1334'

# Enable logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


def job():
    logging.info('Running job...')
    smtp = SMTP(smtp_url=SMTP_URL, smtp_port=SMTP_PORT,
                smtp_email=SMTP_EMAIL, smtp_password=SMTP_PASSWORD)
    email_templates = EmailTemplates()
    last_names = LAST_NAMES.split(',')
    number_of_found_obituaries = 0

    for last_name in last_names:
        search_results = requests.get(SEARCH_URL_TEMPLATE.format(
            last_name), headers={'User-Agent': USER_AGENT})

        if search_results.status_code == 200:
            if search_results.text.find(NO_RESULTS_TEMPLATE.format(last_name)) == -1:
                subject = "A member of the {} family has passed away.".format(
                    last_name)
                body = email_templates.generate_basic_template(dict(email_greeting=EMAIL_GREETING, last_name=last_name, search_url=SEARCH_URL_TEMPLATE.format(
                    last_name)))
                smtp.send_email(from_email=FROM_EMAIL,
                                to_email=TO_EMAIL, subject=subject, body=body)
                number_of_found_obituaries += 1
        elif search_results.status_code in [400, 401, 403, 429, 500, 502, 503, 504]:
            subject = "check-obituaries.py encountered an error from server"
            body = email_templates.generate_error_template(
                dict(email_greeting=EMAIL_GREETING, status_code=search_results.status_code))
            smtp.send_email(from_email=FROM_EMAIL,
                            to_email=TO_EMAIL, subject=subject, body=body)
            logging.error(
                'An error has occurred on the server when searching for: {}'.format(last_name))

    if number_of_found_obituaries == 0:
        logging.info('No new obituary was found.')
        logging.info('Job finished.')
    else:
        logging.info('{} obituaries have been found.'.format(
            str(number_of_found_obituaries)))
        logging.info('Job finished.')


schedule.every().day.at('15:00').do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
