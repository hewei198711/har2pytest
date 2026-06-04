import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreInfoDetail(params=params, headers=headers):
    """
    服务中心详情 -- 服务中心资料
    /mgmt/store/getStoreInfoDetail

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/store/getStoreInfoDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
