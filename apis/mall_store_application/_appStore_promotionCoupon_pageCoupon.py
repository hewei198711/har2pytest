import os

from util.client import client

params = {
    "asc": False,  # 是否升序:true-升序,false-降序
    "cardNo": "",  # 会员卡号
    "couponName": "",  # 优惠券名称
    "couponNumber": "",  # 优惠券编号
    "dataMonth": "",  # 销售呈报月份(yyyy-MM)
    "effective": False,  # 资格有效期
    "endTime": "",  # 优惠券结束时间(yyyy-MM-dd HH:mm:ss)
    "expireDays": 0,  # 失效到期时间
    "mobile": "",  # 会员电话
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "realName": "",  # 会员姓名
    "sortBy": 0,  # 排序字段:1-失效到期时间,2-生效时间,3-失效时间
    "startTime": "",  # 优惠券开始时间(yyyy-MM-dd HH:mm:ss)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_promotionCoupon_pageCoupon(params=params, headers=headers):
    """
    分页查询优惠券列表
    /appStore/promotionCoupon/pageCoupon

    参数说明:
    - asc: 是否升序:true-升序,false-降序
    - cardNo: 会员卡号
    - couponName: 优惠券名称
    - couponNumber: 优惠券编号
    - dataMonth: 销售呈报月份(yyyy-MM)
    - effective: 资格有效期
    - endTime: 优惠券结束时间(yyyy-MM-dd HH:mm:ss)
    - expireDays: 失效到期时间
    - mobile: 会员电话
    - realName: 会员姓名
    - sortBy: 排序字段:1-失效到期时间,2-生效时间,3-失效时间
    - startTime: 优惠券开始时间(yyyy-MM-dd HH:mm:ss)
    """

    url = "/appStore/promotionCoupon/pageCoupon"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
