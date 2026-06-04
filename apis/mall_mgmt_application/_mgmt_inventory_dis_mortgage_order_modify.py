import os

from util.client import client

data = {
    "orderRemark": "",  # 押货单备注
    "orderSn": "",  # 押货单编号
    "productList": [{"mortgageNum": 0, "mortgagePrice": 0.0, "productCode": ""}],  # 押货单商品列表信息
    "pushMark": "",  # 不用传
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_modify(data=data, headers=headers):
    """
    押货单修改
    /mgmt/inventory/dis/mortgage/order/modify

    参数说明:
    - orderRemark: 押货单备注
    - orderSn: 押货单编号
    - productList: 押货单商品列表信息
    - productList.mortgageNum: 押货商品数量
    - productList.mortgagePrice: 商品押货价
    - productList.productCode: 商品编码
    - pushMark: 不用传
    """

    url = "/mgmt/inventory/dis/mortgage/order/modify"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
