import os
from urllib.parse import urlencode

from util.client import client

data = {
    "maxDownloadTimes": 0,  # maxDownloadTimes
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_authorization_updateMaxDownloadTimes(data=data, headers=headers):
    """
    更新所有授权书可下载次数
    /mgmt/store/authorization/updateMaxDownloadTimes

    参数说明:
    - maxDownloadTimes: maxDownloadTimes
    """

    url = "/mgmt/store/authorization/updateMaxDownloadTimes"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
