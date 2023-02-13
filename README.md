# check-obituaries

Need something that notifies you when people die? This script is will check legacy.com every 24 hours for a new obituary against a list of names which is passed in as a json string. Once one found, an email will be sent.

## How to Run

1. Download repo
    - `git checkout develop`
    - `git pull`
    - `cd check-obituaries`
2. Export environment variables
3. run docker-compose
    - `docker-compose up --build -d`
