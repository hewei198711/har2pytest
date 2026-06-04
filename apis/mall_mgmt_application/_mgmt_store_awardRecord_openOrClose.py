import os

from util.client import client

params = {
    "flag": 0,  # flag
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_awardRecord_openOrClose(params=params, headers=headers):
    """
    关闭/打开海报水印展示 0 打开 1 关闭
    /mgmt/store/awardRecord/openOrClose

    参数说明:
    - flag: flag
    """

    url = "/mgmt/store/awardRecord/openOrClose"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
