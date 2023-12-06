from datetime import date, timedelta
import requests

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
LEGACY_COM_API_URL = "https://www.legacy.com/api/_frontend/search?cityIdList={city_id}&regionIdList={region_id}&countryIdList={country_id}&endDate={today}&firstName=&keyword=&lastName={last_name}&limit=50&noticeType=all&session_id=&startDate={yesterday}"


class LegacyComApiError(Exception):
    pass


class LegacyComApi:
    def __init__(self, city_id, region_id, country_id, last_names_comma_delimited):
        assert len(city_id) > 0 and city_id.isnumeric()
        assert len(region_id) > 0 and region_id.isnumeric()
        assert len(country_id) > 0 and country_id.isnumeric()
        assert len(last_names_comma_delimited) > 0

        today = date.today().isoformat()
        yesterday = date.today() - timedelta(days=1)
        last_names = last_names_comma_delimited.split(",")

        self.legacy_com_api_entries = []

        for last_name in last_names:
            legacy_com_api_entry = {}
            legacy_com_api_entry["last_name"] = last_name
            legacy_com_api_entry["constructed_legacy_url"] = LEGACY_COM_API_URL.format(
                city_id=city_id,
                region_id=region_id,
                country_id=country_id,
                last_name=last_name,
                today=today,
                yesterday=yesterday
            )

            self.legacy_com_api_entries.append(legacy_com_api_entry)

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
