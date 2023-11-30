# Check Obituaries

Need something that notifies you when people die? This script is will check legacy.com every 24 hours for a new obituary against a list of names which is passed in as a json string. Once one found, an email will be sent.

## Setup

1. Download repo
    - `git checkout develop`
    - `git pull`
    - `cd check-obituaries`
2. Export environment variables
3. run docker-compose
    - `docker-compose up --build -d`

## Email Templates

The script reads in email templates everytime it is ran. You can customize the templates located in the _templates_ folder. They are read in as HTML files and are injected at runtime with the information.

### Structure

-   error.html - Error Template
-   index.html - Main Template

## Environment Variables

| Variable       | Required | Default | Example                        | Needed by                     |
| -------------- | -------- | ------- | ------------------------------ | ----------------------------- |
| LAST_NAMES     | true     | ---     | Smith,Ford,James               | Legacy Obituary Website       |
| FROM_EMAIL     | true     | ---     | from@example.com               | SMTP Server (send email from) |
| TO_EMAIL       | true     | ---     | to@example.com                 | SMTP Server (send email to)   |
| EMAIL_GREETING | true     | ---     | Laura                          | Template                      |
| SMTP_URL       | true     | ---     | smtp.example.com               | SMTP Server                   |
| SMTP_PORT      | true     | ---     | 465                            | SMTP Server                   |
| SMTP_EMAIL     | true     | ---     | laura@example.com              | SMTP Server                   |
| SMTP_PASSWORD  | true     | ---     | 8f5cd6729h0v5d247vc190ddcs4l2a | SMTP Server                   |

**NOTE:** For security purposes, it is strong recommended that you use a generated API passwords.
