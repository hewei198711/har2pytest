import os

from util.client import client

params = {
    "dataType": "",  # 数据类型
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dict_getWebDictData(params=params, headers=headers):
    """
    getWebDictData
    /mgmt/dict/getWebDictData

    参数说明:
    - dataType: 数据类型
    """

    url = "/mgmt/dict/getWebDictData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
