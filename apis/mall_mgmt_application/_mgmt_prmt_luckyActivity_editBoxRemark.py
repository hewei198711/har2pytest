import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "remark": "",  # 文案
    "remarkCode": "",  # 文案编码
    "state": 0,  # 上下架状态：1-上架  2-下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_editBoxRemark(data=data, headers=headers):
    """
    编辑盲盒海报文案
    /mgmt/prmt/luckyActivity/editBoxRemark

    参数说明:
    - id: 主键id
    - remark: 文案
    - remarkCode: 文案编码
    - state: 上下架状态：1-上架  2-下架
    """

    url = "/mgmt/prmt/luckyActivity/editBoxRemark"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
