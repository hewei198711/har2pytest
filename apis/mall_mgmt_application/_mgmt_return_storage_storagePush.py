import os
from urllib.parse import urlencode

from util.client import client

data = {
    "ids": [],  # ids
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_return_storage_storagePush(data=data, headers=headers):
    """
    推送退货入仓
    /mgmt/return/storage/storagePush

    参数说明:
    - ids: ids
    """

    url = "/mgmt/return/storage/storagePush"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
