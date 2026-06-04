import os

from util.client import client

data = {
    "customPrice": 0.0,  # 画线价(赠品类型)
    "isGift": False,  # 是否赠品
    "productGroupIndex": 0,  # 主产品分组序号
    "promotionId": 0,  # 随心购活动id
    "serialNo": "",  # 产品编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_libertySale_addProduct(data=data, headers=headers):
    """
    详情与编辑页面-手动添加商品
    /mgmt/prmt/libertySale/addProduct

    参数说明:
    - customPrice: 画线价(赠品类型)
    - isGift: 是否赠品
    - productGroupIndex: 主产品分组序号
    - promotionId: 随心购活动id
    - serialNo: 产品编码
    """

    url = "/mgmt/prmt/libertySale/addProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
