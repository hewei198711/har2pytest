import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_searchByStoreCode(params=params, headers=headers):
    """
    通过storeCode获取相关信息(新建合同搜索需要)
    /mgmt/store/searchByStoreCode

    参数说明:
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/searchByStoreCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
