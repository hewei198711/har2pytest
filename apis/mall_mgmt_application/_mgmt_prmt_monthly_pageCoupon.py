import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "couponName": "",  # 优惠券名称
    "couponNumber": "",  # 优惠券编号
    "dataMonthEnd": "",  # 达标月份止区
    "dataMonthStart": "",  # 达标月份起区
    "mobile": "",  # 会员电话
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_monthly_pageCoupon(params=params, headers=headers):
    """
    分页查询优惠券月结数据
    /mgmt/prmt/monthly/pageCoupon

    参数说明:
    - cardNo: 会员卡号
    - couponName: 优惠券名称
    - couponNumber: 优惠券编号
    - dataMonthEnd: 达标月份止区
    - dataMonthStart: 达标月份起区
    - mobile: 会员电话
    - storeCode: 服务中心编号
    """

    url = "/mgmt/prmt/monthly/pageCoupon"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
