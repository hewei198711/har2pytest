import os

from util.client import client

params = {
    "couponName": "",  # 优惠券名称
    "couponNumber": "",  # 优惠券编码
    "createTimeMax": "",  # 创建时间大
    "createTimeMin": "",  # 创建时间小
    "grantEndTime": "",  # 派发结束时间
    "grantStartTime": "",  # 派发开始时间
    "grantTarget": 0,  # 派发对象1所有人2身份3等级4导入
    "grantType": 0,  # 派发方式:1-即时派发,2-定时派发,3-每日循环派发,4-每月定时派发,5-对接外部系统,6-对接企微系统
    "grantWay": 0,  # 派发类型1普通派发2转赠派发
    "ids": [],  # 派发记录id
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "state": 0,  # 发放状态1待审核2派发中3已完成4已驳回5草稿6已停止
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_getCouponGrantList(params=params, headers=headers):
    """
    分页查询派发记录
    /mgmt/prmt/couponGrant/getCouponGrantList

    参数说明:
    - couponName: 优惠券名称
    - couponNumber: 优惠券编码
    - createTimeMax: 创建时间大
    - createTimeMin: 创建时间小
    - grantEndTime: 派发结束时间
    - grantStartTime: 派发开始时间
    - grantTarget: 派发对象1所有人2身份3等级4导入
    - grantType: 派发方式:1-即时派发,2-定时派发,3-每日循环派发,4-每月定时派发,5-对接外部系统,6-对接企微系统
    - grantWay: 派发类型1普通派发2转赠派发
    - ids: 派发记录id
    - pageNum: 当前页
    - pageSize: 每页数量
    - state: 发放状态1待审核2派发中3已完成4已驳回5草稿6已停止
    """

    url = "/mgmt/prmt/couponGrant/getCouponGrantList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
