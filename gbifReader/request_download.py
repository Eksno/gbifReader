import requests
from datetime import datetime
import dateutil.relativedelta
from requests.auth import HTTPBasicAuth


def send_request(first_year=None, first_month=None, last_update=None):
    print("\nRequesting data from gbif...")
    print(" - Generating query...")

    url = "https://api.gbif.org/v1/occurrence/download/request"

    if first_year is first_month is last_update is None:
        d = datetime.now() - dateutil.relativedelta.relativedelta(months=1)
        query_dict = {
            "format": "SIMPLE_CSV",
            "predicate":
            {
                "type": "and",
                "predicates":
                [
                    {
                        "type": "greaterThanOrEquals",
                        "key": "YEAR",
                        "value": d.year
                    },
                    {
                        "type": "greaterThanOrEquals",
                        "key": "MONTH",
                        "value": d.month
                    }
                ]
            }
        }
    else:
        query_dict = {
            "format": "SIMPLE_CSV",
            "predicate":
            {
                "type": "and",
                "predicates":
                [
                    {
                        "type": "greaterThanOrEquals",
                        "key": "YEAR",
                        "value": first_year
                    },
                    {
                        "type": "greaterThanOrEquals",
                        "key": "MONTH",
                        "value": first_month
                    },
                    {
                        "type": "greaterThan",
                        "key": "LAST_INTERPRETED",
                        "value": last_update
                    }
                ]
            }
        }

    print(" - Sending request...")
    headers = {'Content-Type': 'application/json'}

    user, passwd = input(" - username: "), input(" - password: ")
    r = requests.post(url, headers=headers, json=query_dict, auth=HTTPBasicAuth(user, passwd))
    dowload_id = ''.join(list(str(r.content))[2:-1])
    print(f" / Data request sent. Dowload Id = `{dowload_id}`.")
    return dowload_id
