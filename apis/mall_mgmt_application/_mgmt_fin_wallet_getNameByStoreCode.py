import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_getNameByStoreCode(params=params, headers=headers):
    """
    根据服务中心编号获取服务中心名称
    /mgmt/fin/wallet/getNameByStoreCode

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/fin/wallet/getNameByStoreCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
