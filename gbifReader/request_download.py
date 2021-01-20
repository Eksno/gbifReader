import requests
from datetime import datetime
import dateutil.relativedelta
from requests.auth import HTTPBasicAuth


def send_request():
    url = "https://api.gbif.org/v1/occurrence/download/request"

    d = datetime.now() - dateutil.relativedelta.relativedelta(months=1)

    query_dict = {
      "format": "SIMPLE_CSV",
      "predicate":
      {
        "type": "and",
        "predicates":
        [
          {
            "type": "equals",
            "key": "YEAR",
            "value": d.year
          },
          {
            "type": "equals",
            "key": "MONTH",
            "value": d.month
          }
        ]
      }
    }

    headers = {'Content-Type': 'application/json'}

    user, passwd = input("username: "), input("password: ")
    r = requests.post(url, headers=headers, json=query_dict, auth=HTTPBasicAuth(user, passwd))

    return ''.join(list(str(r.content))[2:-1])
