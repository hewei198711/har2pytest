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


def _appStore_store_dis_mortgageOrder_modify(data=data, headers=headers):
    """
    押货单修改
    /appStore/store/dis/mortgageOrder/modify

    参数说明:
    - orderRemark: 押货单备注
    - orderSn: 押货单编号
    - productList: 押货单商品列表信息
    - productList.mortgageNum: 押货商品数量
    - productList.mortgagePrice: 商品押货价
    - productList.productCode: 商品编码
    - pushMark: 不用传
    """

    url = "/appStore/store/dis/mortgageOrder/modify"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
