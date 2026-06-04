import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_common_fetchStoreAndCompanyInfo(params=params, headers=headers):
    """
    获取上门取件相关默认参数
    /mgmt/inventory/common/fetchStoreAndCompanyInfo

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/common/fetchStoreAndCompanyInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
