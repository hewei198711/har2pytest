import os

from util.client import client

params = {
    "id": 0,  # 活动主键
    "input": "",  # 输入内容
    "target": 0,  # 输入目标:1-活动名称,2-活动编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shoppedGift_checkInputExists(params=params, headers=headers):
    """
    校验输入内容是否已存在
    /mgmt/prmt/shoppedGift/checkInputExists

    参数说明:
    - id: 活动主键
    - input: 输入内容
    - target: 输入目标:1-活动名称,2-活动编码
    """

    url = "/mgmt/prmt/shoppedGift/checkInputExists"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
