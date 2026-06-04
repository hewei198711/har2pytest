import os

from util.client import client

params = {
    "businessMode": 0,  # businessMode
    "creatorCard": "",  # creatorCard
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_leader_existsByStoreInfo(params=params, headers=headers):
    """
    店铺转让-光标离开时触发
    /mgmt/store/leader/existsByStoreInfo

    参数说明:
    - businessMode: businessMode
    - creatorCard: creatorCard
    - storeCode: storeCode
    """

    url = "/mgmt/store/leader/existsByStoreInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
