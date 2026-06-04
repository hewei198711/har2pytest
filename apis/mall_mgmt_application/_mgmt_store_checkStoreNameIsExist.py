import os

from util.client import client

params = {
    "memberType": 0,  # memberType
    "storeName": "",  # storeName
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_checkStoreNameIsExist(params=params, headers=headers):
    """
    检查服务中心名称是否存在, code=500时，存在相同值，提示语取message
    /mgmt/store/checkStoreNameIsExist

    参数说明:
    - memberType: memberType
    - storeName: storeName
    """

    url = "/mgmt/store/checkStoreNameIsExist"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
