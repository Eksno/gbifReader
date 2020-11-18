import request_download
import requests
from zipfile import ZipFile
from io import BytesIO

DOWNLOAD_ID = request_download.send_request()

r = requests.get("https://api.gbif.org/v1/occurrence/download/request/{}.zip".format(DOWNLOAD_ID))

zipfile = ZipFile(BytesIO(r.content))

filenames = zipfile.namelist()

csv = zipfile.open(filenames[0]).read()

with open('data.csv', 'wb') as f:
    f.write(csv)
