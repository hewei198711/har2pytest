import os

from util.client import client

params = {
    "couponType": 0,  # 优惠券类型:1-立减券,2-满减券,3-叠加满减券,4-堆叠满减券,5-产品兑换券
    "serialNo": "",  # 查询的产品编码
    "serialNos": [],  # 原产品列表
    "type": 0,  # 可用列表1不可用列表2
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_selectProduct(params=params, headers=headers):
    """
    查询商品加入可用或不可用商品列表
    /mgmt/prmt/coupon/selectProduct

    参数说明:
    - couponType: 优惠券类型:1-立减券,2-满减券,3-叠加满减券,4-堆叠满减券,5-产品兑换券
    - serialNo: 查询的产品编码
    - serialNos: 原产品列表
    - type: 可用列表1不可用列表2
    """

    url = "/mgmt/prmt/coupon/selectProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
