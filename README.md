# Check Obituaries Script

Need something that notifies you when they appear in an obituary? This script is will check legacy.com every 24 hours (default is 13:00) for a new obituary against a list of names which is passed in as a json string. Once one found, an email will be sent.

## Setup

1. Download repo
    - `git checkout develop`
    - `git pull`
    - `cd check-obituaries`
2. Export environment variables
3. run docker-compose
    - `docker-compose up --build -d`

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

| Variable        | Required | Default | Example                        | Needed by                     |
| --------------- | -------- | ------- | ------------------------------ | ----------------------------- |
| SCRIPT_RUN_TIME | false    | 13:00   | 00:00 - 23:59                  | Scheduler                     |
| FROM_EMAIL      | true     | ---     | from@example.com               | SMTP Server (send email from) |
| TO_EMAIL        | true     | ---     | to@example.com                 | SMTP Server (send email to)   |
| EMAIL_GREETING  | true     | ---     | Laura                          | Template                      |
| SMTP_URL        | true     | ---     | smtp.example.com               | SMTP Server                   |
| SMTP_PORT       | true     | ---     | 465                            | SMTP Server                   |
| SMTP_EMAIL      | true     | ---     | laura@example.com              | SMTP Server                   |
| SMTP_PASSWORD   | true     | ---     | 8f5cd6729h0v5d247vc190ddcs4l2a | SMTP Server                   |

**NOTE:** For security purposes, it is strong recommended that you use a generated API passwords.
