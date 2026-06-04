import os

from util.client import client

params = {
    "shopKeeperNo": "",  # shopKeeperNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_checkShopKeeperNoIsExist(params=params, headers=headers):
    """
    检查管理员卡号是否存在，true为存在相同值
    /mgmt/store/checkShopKeeperNoIsExist

    参数说明:
    - shopKeeperNo: shopKeeperNo
    """

    url = "/mgmt/store/checkShopKeeperNoIsExist"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
