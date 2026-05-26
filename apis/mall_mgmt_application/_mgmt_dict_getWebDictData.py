import os

from util.client import client

params = {
    "dataType": "AUDIT_STAUTS",  # 数据类型
}

headers = {
    "channel": "pc",
    "client": "op",
    "authorization": f"bearer {os.environ['access_token']}",
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
