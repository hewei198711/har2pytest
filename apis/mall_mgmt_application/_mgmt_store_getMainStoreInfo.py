import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getMainStoreInfo(params=params, headers=headers):
    """
    根据服务中心编号获取服务信息--仅仅主表信息
    /mgmt/store/getMainStoreInfo

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/store/getMainStoreInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
