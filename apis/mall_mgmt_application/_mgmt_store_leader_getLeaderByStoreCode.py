import os

from util.client import client

params = {
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_leader_getLeaderByStoreCode(params=params, headers=headers):
    """
    根据店铺编号获取负责人信息
    /mgmt/store/leader/getLeaderByStoreCode

    参数说明:
    - storeCode: 店铺编号
    """

    url = "/mgmt/store/leader/getLeaderByStoreCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
