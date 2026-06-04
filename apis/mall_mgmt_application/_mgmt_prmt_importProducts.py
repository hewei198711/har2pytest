import os
from urllib.parse import urlencode

from util.client import client

data = {
    "file": "",  # 产品文件
    "limitNumber": 0,  # 限购数量(-1不限,-2按需分配)
    "limitType": 0,  # 限购方式1不限量2独立限量3统一限量4按需导入5按阶梯配置独立限量6按阶梯配置统一限量
    "pointSteps": [],  # 活动PV阶梯集合
    "promotionId": 0,  # 活动id
    "promotionType": 0,  # 活动类型1活动2换购4预售
    "serialNos": [],  # 已加入商品
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_importProducts(data=data, headers=headers):
    """
    导入活动产品
    /mgmt/prmt/importProducts

    参数说明:
    - file: 产品文件
    - limitNumber: 限购数量(-1不限,-2按需分配)
    - limitType: 限购方式1不限量2独立限量3统一限量4按需导入5按阶梯配置独立限量6按阶梯配置统一限量
    - pointSteps: 活动PV阶梯集合
    - promotionId: 活动id
    - promotionType: 活动类型1活动2换购4预售
    - serialNos: 已加入商品
    """

    url = "/mgmt/prmt/importProducts"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
