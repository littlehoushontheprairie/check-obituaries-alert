import os
from datetime import date, timedelta
import requests
import json

"""
Legacy.com API

This class encapsulates the API call to check Legacy.com.

countryId - Country ID (i.e. 1 - United States)
regionId - Region ID. These are states or provinces. (i.e. 29 - New York) 
    - This can be found with this endpoint: https://www.legacy.com/api/_frontend/regions/country/united-states
cityId - City ID.
    - This can be found with this endpoint: https://www.legacy.com/api/_frontend/cities/region/{regionId}

"""

USER_AGENT: str = "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"
LEGACY_COM_API_BASE_URL: str = "https://www.legacy.com/api/_frontend/search?endDate={today}&startDate={yesterday}&firstName={first_name}&lastName={last_name}&session_id=&keyword=&limit=50&noticeType=all"


class LegacyComApiError(Exception):
    pass


class LegacyComApiMissingParameterError(Exception):
    pass


class LegacyComApi:
    def __init__(self):
        self.obituaries: list = []

        data: dict = {"searchParameters": []}

        filePath: str = "/data/legacy_com_search_parameters.json"

        if not os.path.exists(filePath):
            with open(filePath, 'w') as file:
                json.dump({"searchParameters": []}, file)
        else:
            with open(filePath, "r") as json_data:
                data = json.load(json_data)

        searchParameters: dict = data.get("searchParameters")

        today: str = date.today().isoformat()
        yesterday: str = (date.today() - timedelta(days=1)).isoformat()

        for searchParameter in searchParameters:
            if searchParameter.get("firstName", None) is not None or searchParameter.get("lastName", None) is not None:
                # Construct url for API call
                constructed_legacy_api_url: str = LEGACY_COM_API_BASE_URL.format(
                    first_name=searchParameter.get("firstName", ""),
                    last_name=searchParameter.get("lastName", ""),
                    today=today,
                    yesterday=yesterday
                )

                if searchParameter.get("countryId", None) is not None:
                    constructed_legacy_api_url = constructed_legacy_api_url + \
                        "&countryIdList=" + \
                        str(searchParameter.get("countryId", ""))

                if searchParameter.get("regionId", None) is not None:
                    constructed_legacy_api_url = constructed_legacy_api_url + \
                        "&regionIdList=" + \
                        str(searchParameter.get("regionId", ""))

                if searchParameter.get("cityId", None) is not None:
                    constructed_legacy_api_url = constructed_legacy_api_url + \
                        "&cityIdList=" + str(searchParameter.get("cityId", ""))

                # Making call to Legacy.com API using constructed url
                response = requests.get(constructed_legacy_api_url, headers={
                                        "User-Agent": USER_AGENT})

                if response.status_code == 200:
                    entries = response.json()["obituaries"]

                    for entry in entries:
                        obituary = {}
                        obituary["full_name"] = entry["name"]["fullName"]
                        obituary["obituary_snippet"] = entry["obitSnippet"]
                        obituary["link"] = entry["links"]["obituaryUrl"]["href"]
                        obituary["published_on"] = entry["publishedLine"]
                        self.obituaries.append(obituary)

                elif response.status_code in [400, 401, 403, 404, 429, 500, 502, 503, 504]:
                    raise LegacyComApiError(
                        "Legacy.com API has entered an en error.", response.status_code)

            else:
                raise LegacyComApiMissingParameterError(
                    "Legacy.com API has entered an en error.", "Legacy.com API requires a first name or last name.")
