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

USER_AGENT = "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1"
LEGACY_COM_API_BASE_URL = "https://www.legacy.com/api/_frontend/search?endDate={today}&firstName={first_name}&keyword=&lastName={last_name}&limit=50&noticeType=all&session_id=&startDate=2002-02-02"


class LegacyComApiError(Exception):
    pass


class LegacyComApiMissingParameterError(Exception):
    pass


class LegacyComApi:
    def __init__(self):
        data = {}

        with open("legacy_com_search_parameters.json", "r") as json_data:
            data = json.load(json_data)

        searchParameters = data["searchParameters"]

        today = date.today().isoformat()
        yesterday = date.today() - timedelta(days=1)

        self.legacy_com_api_entries = []

        for searchParameter in searchParameters:
            legacy_com_api_entry = {}

            if searchParameter.get("firstName", None) is not None or searchParameter.get("lastName", None) is not None:
                legacy_com_api_entry["constructed_legacy_url"] = LEGACY_COM_API_BASE_URL.format(
                    first_name=searchParameter.get("firstName", ""),
                    last_name=searchParameter.get("lastName", ""),
                    today=today,
                    yesterday=yesterday
                )

                if searchParameter.get("countryId", None) is not None:
                    legacy_com_api_entry["constructed_legacy_url"] = legacy_com_api_entry["constructed_legacy_url"] + \
                        "&countryIdList=" + \
                        str(searchParameter.get("countryId", ""))

                if searchParameter.get("regionId", None) is not None:
                    legacy_com_api_entry["constructed_legacy_url"] = legacy_com_api_entry["constructed_legacy_url"] + \
                        "&regionIdList=" + \
                        str(searchParameter.get("regionId", ""))

                if searchParameter.get("cityId", None) is not None:
                    legacy_com_api_entry["constructed_legacy_url"] = legacy_com_api_entry["constructed_legacy_url"] + \
                        "&cityIdList=" + str(searchParameter.get("cityId", ""))

                print(legacy_com_api_entry["constructed_legacy_url"])

                self.legacy_com_api_entries.append(legacy_com_api_entry)
            else:
                raise LegacyComApiMissingParameterError(
                    "Legacy.com API has entered an en error.", "Legacy.com API requires a first name or last name.")

    def call(self):
        obituaries = []

        for legacy_com_api_entry in self.legacy_com_api_entries:
            response = requests.get(legacy_com_api_entry["constructed_legacy_url"], headers={
                                    "User-Agent": USER_AGENT})

            if response.status_code == 200:
                entries = response.json()["obituaries"]

                for entry in entries:
                    obituary = {}
                    obituary["full_name"] = entry["name"]["fullName"]
                    obituary["obituary_snippet"] = entry["obitSnippet"]
                    obituary["link"] = entry["links"]["obituaryUrl"]["href"]
                    obituary["published_on"] = entry["publishedLine"]
                    obituaries.append(obituary)

            elif response.status_code in [400, 401, 403, 404, 429, 500, 502, 503, 504]:
                raise LegacyComApiError(
                    "Legacy.com API has entered an en error.", response.status_code)

        return obituaries
