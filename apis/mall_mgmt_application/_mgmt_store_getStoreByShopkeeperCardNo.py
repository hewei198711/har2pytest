import os

from util.client import client

params = {
    "shopkeeperCardNo": "",  # shopkeeperCardNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreByShopkeeperCardNo(params=params, headers=headers):
    """
    根据服务中心店长卡号获取服务中心
    /mgmt/store/getStoreByShopkeeperCardNo

    参数说明:
    - shopkeeperCardNo: shopkeeperCardNo
    """

    url = "/mgmt/store/getStoreByShopkeeperCardNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
