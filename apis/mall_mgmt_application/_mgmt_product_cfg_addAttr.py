import os

from util.client import client

data = {
    "attrKey": "",  # 属性名
    "attrType": 0,  # 类型：1-文本，2-单选，3-多选
    "attrValArray": [],  # 属性内容数组
    "id": 0,  # 节点id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_cfg_addAttr(data=data, headers=headers):
    """
    产品属性新增
    /mgmt/product/cfg/addAttr

    参数说明:
    - attrKey: 属性名
    - attrType: 类型：1-文本，2-单选，3-多选
    - attrValArray: 属性内容数组
    - id: 节点id
    """

    url = "/mgmt/product/cfg/addAttr"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
