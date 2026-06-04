import os

from util.client import client

params = {
    "flag": 0,  # flag
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_awardRecord_isShowPc(params=params, headers=headers):
    """
    是否显示于门店列表 0 是 1 否
    /mgmt/store/awardRecord/isShowPc

    参数说明:
    - flag: flag
    - id: id
    """

    url = "/mgmt/store/awardRecord/isShowPc"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
