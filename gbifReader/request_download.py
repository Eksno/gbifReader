import requests
from requests.auth import HTTPBasicAuth


def send_request():
    url = "https://api.gbif.org/v1/occurrence/download/request"

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
            "value": "2020"
          },
          {
            "type": "equals",
            "key": "MONTH",
            "value": "11"
          }
        ]
      }
    }

    headers = {'Content-Type': 'application/json'}

    user, passwd = input("username: "), input("password: ")
    r = requests.post(url, headers=headers, json=query_dict, auth=HTTPBasicAuth(user, passwd))

    return ''.join(list(str(r.content))[2:-2])
