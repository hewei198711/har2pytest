import os

from util.client import client

params = {
    "keyword": "",  # 关键字
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getStoreOption(params=params, headers=headers):
    """
    获取服务中心(根据名称或编码模糊搜索)
    /mgmt/store/getStoreOption

    参数说明:
    - keyword: 关键字
    """

    url = "/mgmt/store/getStoreOption"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
