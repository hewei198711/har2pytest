import os

from util.client import client

data = {
    "deliveryDate": "",  # 预计发货时间
    "getCounts": [],  # 可购买数量集合
    "id": 0,  # id:手动新增为活动id，编辑为行记录id
    "originalPrice": 0.0,  # 原价
    "productName": "",  # 产品名称
    "serialNo": "",  # 产品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_unlimited_updateOriginalPrice(data=data, headers=headers):
    """
    编辑商品原价
    /mgmt/prmt/unlimited/updateOriginalPrice

    参数说明:
    - deliveryDate: 预计发货时间
    - getCounts: 可购买数量集合
    - id: id:手动新增为活动id，编辑为行记录id
    - originalPrice: 原价
    - productName: 产品名称
    - serialNo: 产品编码
    """

    url = "/mgmt/prmt/unlimited/updateOriginalPrice"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
