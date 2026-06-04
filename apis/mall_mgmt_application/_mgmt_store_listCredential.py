import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_listCredential(params=params, headers=headers):
    """
    获取服务中心证件
    /mgmt/store/listCredential

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/store/listCredential"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
