import os

from util.client import client

params = {
    "dataType": "",  # 数据类型
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dict_getAppDictData(params=params, headers=headers):
    """
    getAppDictData
    /mgmt/dict/getAppDictData

    参数说明:
    - dataType: 数据类型
    """

    url = "/mgmt/dict/getAppDictData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
