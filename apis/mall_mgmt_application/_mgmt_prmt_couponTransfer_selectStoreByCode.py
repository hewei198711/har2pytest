import os

from util.client import client

params = {
    "code": "",  # code
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponTransfer_selectStoreByCode(params=params, headers=headers):
    """
    根据门店编号搜索门店信息
    /mgmt/prmt/couponTransfer/selectStoreByCode

    参数说明:
    - code: code
    """

    url = "/mgmt/prmt/couponTransfer/selectStoreByCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
