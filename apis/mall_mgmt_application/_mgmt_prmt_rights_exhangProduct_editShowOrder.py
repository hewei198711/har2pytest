import os

from util.client import client

data = {
    "showOrder": 0,  # 展示顺序
    "verId": "",  # 兑换产品版本id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_rights_exhangProduct_editShowOrder(data=data, headers=headers):
    """
    兑换产品版本修改展示顺序
    /mgmt/prmt/rights/exhangProduct/editShowOrder

    参数说明:
    - showOrder: 展示顺序
    - verId: 兑换产品版本id
    """

    url = "/mgmt/prmt/rights/exhangProduct/editShowOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
