import os
from urllib.parse import urlencode

from util.client import client

data = {
    "recordId": "",  # recordId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_download_retry(data=data, headers=headers):
    """
    重试
    /mgmt/download/retry

    参数说明:
    - recordId: recordId
    """

    url = "/mgmt/download/retry"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
