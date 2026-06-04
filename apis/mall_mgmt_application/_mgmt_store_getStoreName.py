import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreName(params=params, headers=headers):
    """
    根据服务中心编号获取服务中心名称(正常服务中心)
    /mgmt/store/getStoreName

    参数说明:
    - storeCode: 服务中心编码
    """

    url = "/mgmt/store/getStoreName"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
