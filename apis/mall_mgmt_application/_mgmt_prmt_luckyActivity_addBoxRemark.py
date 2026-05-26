import os

from util.client import client

data = {
    "remarkCode": "0919010000",  # 文案编码
    "remark": "我是一二三四五六七八九十我是一二三四五六七八九十我是一二三四五六七八九十我是一二三四hhewe十12",  # 文案
    "state": 1,  # 上下架状态：1-上架  2-下架
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_prmt_luckyActivity_addBoxRemark(data=data, headers=headers):
    """
    新增盲盒海报文案
    /mgmt/prmt/luckyActivity/addBoxRemark

    参数说明:
    - id: 主键id
    - remark: 文案
    - remarkCode: 文案编码
    - state: 上下架状态：1-上架  2-下架
    """

    url = "/mgmt/prmt/luckyActivity/addBoxRemark"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
