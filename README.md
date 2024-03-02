# Check Obituaries Alert

Need something that alerts you when they appear in an obituary? This script is will check legacy.com every 24 hours (default is 13:00) for a new obituary against a list of names which is passed in as a json string. Once one found, an email will be sent.

## Setup

#### Running Locally

1. Download repo
    - `git clone https://github.com/littlehoushontheprairie/check-obituaries-alert.git`
    - `git checkout develop`
    - `git pull`
    - `cd check-obituaries-alert`
2. Export environment variables
3. Run
    - `python3 check-obituaries-alert.py`

#### Building and Running as Container from Source

1. Download repo
    - `git checkout develop`
    - `git pull`
    - `cd check-obituaries-alert`
2. Export environment variables
3. run docker-compose
    - `docker-compose up --build -d`

#### Running Container from GitHub Docker Registry (using Terminal)

1. Download `latest` container
    - `docker pull ghcr.io/littlehoushontheprairie/check-obituaries-alert:latest`
2. Run container
    - ```
      docker run --restart=always -d --network host \
      --name check-obituaries-alert \
      -e TZ="America/Los_Angeles" \
      -e FROM_EMAIL="from@example.com" \
      -e TO_NAME="to" \
      -e TO_EMAIL="to@example.com" \
      -e SMTP_HOST="smtp.example.com" \
      -e SMTP_USER="laura@example.com" \
      -e SMTP_PASSWORD="8f5cd6729h0v5d247vc190ddcs4l2a" \
      ghcr.io/littlehoushontheprairie/check-obituaries-alert:latest
      ```

#### Running Container from GitHub Docker Registry (using docker-compose)

1. Create `docker-compose.yml` file
2. Add content.

    - ```
      version: "3.5"

      services:
          check-obituaries-alert:
              container_name: check-obituaries-alert
              image: ghcr.io/littlehoushontheprairie/check-obituaries-alert:latest
              restart: always
              network_mode: host
              environment:
                  TZ: America/Los_Angeles
                  FROM_EMAIL: "${FROM_EMAIL}"
                  TO_NAME: "${TO_NAME}"
                  TO_EMAIL: "${TO_EMAIL}"
                  SMTP_HOST: "${SMTP_HOST}"
                  SMTP_USER: "${SMTP_USER}"
                  SMTP_PASSWORD: "${SMTP_PASSWORD}"
      ```

3. Export environment variables
4. Run `docker-compose up -d`

## Legacy.com API

The script reads in a json file, [legacy_com_search_parameters.json](./legacy_com_search_parameters.json), which is a json object of names and location ids. The file should be located in `/data` and mapped correctly in the [docker-compose.yml](./docker-compose.yml#L25). Legacy.com API doesn't require all fields to be filled in. At least some need to be.

### Structure

Inside the JSON file, it should be laid as such. Keep in mind that each object in the `searchParameters` only requires either `firstName` or `lastName` to search for a refine search add as many as you need.

```json
{
    "searchParameters": [
        {
            "firstName": "John",
            "lastName": "Smith",
            "countryId": 1,
            "regionId": 29,
            "cityId": 125138
        }
    ]
}
```

`countryId`, `regionId`, and `cityId` can be found on the [Legacy.com](https://www.legacy.com) site, but here are some direct information:

-   `countryId` - Country ID (i.e. 1 - United States)
-   `regionId` - Region ID. These are states or provinces. (i.e. 29 - New York)
    -   This can be found with this endpoint: https://www.legacy.com/api/_frontend/regions/country/united-states
-   `cityId` - City ID. (i.e. 125138 - New York City)
    -   This can be found with this endpoint: https://www.legacy.com/api/_frontend/cities/region/{regionId}

## Email Templates

The script reads in email templates everytime it is ran. You can customize the templates located in the _templates_ folder. They are read in as HTML files and are injected at runtime with the information.

### Structure

-   error.html - Error Template
-   index.html - Main Template

## Environment Variables

| Variable        | Required | Default                | Example                        | Needed by                     |
| --------------- | -------- | ---------------------- | ------------------------------ | ----------------------------- |
| SCRIPT_RUN_TIME | false    | 13:00                  | 00:00 - 23:59                  | Scheduler                     |
| FROM_NAME       | false    | Check Obituaries Alert | Check Obituaries Alert         | SMTP Server (send email from) |
| FROM_EMAIL      | true     | ---                    | from@example.com               | SMTP Server (send email from) |
| TO_NAME         | false    |                        | Laura                          | SMTP Server (send email to)   |
| TO_EMAIL        | true     | ---                    | to@example.com                 | SMTP Server (send email to)   |
| SMTP_HOST       | true     | ---                    | smtp.example.com               | SMTP Server                   |
| SMTP_PORT       | false    | 465                    | 465                            | SMTP Server                   |
| SMTP_EMAIL      | true     | ---                    | laura@example.com              | SMTP Server                   |
| SMTP_PASSWORD   | true     | ---                    | 8f5cd6729h0v5d247vc190ddcs4l2a | SMTP Server                   |

**NOTE:** For security purposes, it is strong recommended that you use a generated API passwords.
