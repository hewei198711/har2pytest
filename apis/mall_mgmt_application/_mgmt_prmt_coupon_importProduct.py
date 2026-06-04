import os
from urllib.parse import urlencode

from util.client import client

data = {
    "couponId": 0,  # 优惠券id
    "couponType": 0,  # 优惠券类型:1-立减券,2-满减券,3-叠加满减券,4-堆叠满减券,5-产品兑换券
    "file": "",  # 产品文件
    "serialNos": [],  # 原产品编码列表
    "type": 0,  # 可用列表1不可用列表2
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_coupon_importProduct(data=data, headers=headers):
    """
    导入优惠券关联的可用或不可用产品（新建或编辑）
    /mgmt/prmt/coupon/importProduct

    参数说明:
    - couponId: 优惠券id
    - couponType: 优惠券类型:1-立减券,2-满减券,3-叠加满减券,4-堆叠满减券,5-产品兑换券
    - file: 产品文件
    - serialNos: 原产品编码列表
    - type: 可用列表1不可用列表2
    """

    url = "/mgmt/prmt/coupon/importProduct"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
