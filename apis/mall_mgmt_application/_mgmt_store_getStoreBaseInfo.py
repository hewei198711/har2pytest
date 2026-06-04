import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreBaseInfo(params=params, headers=headers):
    """
    根据服务中心编号获取服务信息--店铺装修/通讯地址/额外信息/证件资料
    /mgmt/store/getStoreBaseInfo

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/store/getStoreBaseInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
