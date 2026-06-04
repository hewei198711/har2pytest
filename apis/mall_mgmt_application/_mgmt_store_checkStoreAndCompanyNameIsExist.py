import os

from util.client import client

params = {
    "excludeStoreCode": "",  # excludeStoreCode
    "storeName": "",  # storeName
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_checkStoreAndCompanyNameIsExist(params=params, headers=headers):
    """
    检查服务中心名称和服务公司名称是否存在
    /mgmt/store/checkStoreAndCompanyNameIsExist

    参数说明:
    - excludeStoreCode: excludeStoreCode
    - storeName: storeName
    """

    url = "/mgmt/store/checkStoreAndCompanyNameIsExist"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
