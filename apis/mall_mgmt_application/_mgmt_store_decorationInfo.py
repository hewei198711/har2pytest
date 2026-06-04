import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_decorationInfo(params=params, headers=headers):
    """
    服务中心详情 -- 服务中心装修资料
    /mgmt/store/decorationInfo

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/store/decorationInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
