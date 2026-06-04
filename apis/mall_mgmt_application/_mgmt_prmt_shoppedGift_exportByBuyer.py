import os

from util.client import client

params = {
    "buyerCardNo": "",  # 购货人卡号
    "buyerMobile": "",  # 购货人注册手机号
    "buyerRealName": "",  # 购货人姓名
    "couponName": "",  # 优惠券名称
    "grantedTimeEnd": "",  # 派发时间止区(yyyy-MM-dd)
    "grantedTimeStart": "",  # 派发时间起区(yyyy-MM-dd)
    "handlerCardNo": "",  # 经办人卡号
    "handlerMobile": "",  # 经办人注册手机号
    "handlerRealName": "",  # 经办人姓名
    "id": 0,  # 活动id
    "orderNo": "",  # 订单编号
    "orderWay": 0,  # 下单方式:1-自购,2-代购
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "payTimeEnd": "",  # 订单支付时间止区(yyyy-MM-dd)
    "payTimeStart": "",  # 订单支付时间起区(yyyy-MM-dd)
    "returned": False,  # 是否已退货
    "state": 0,  # 派券状态:0-未派发,1-已派发,2-不派发,3-券不足
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shoppedGift_exportByBuyer(params=params, headers=headers):
    """
    导出购货人获券列表
    /mgmt/prmt/shoppedGift/exportByBuyer

    参数说明:
    - buyerCardNo: 购货人卡号
    - buyerMobile: 购货人注册手机号
    - buyerRealName: 购货人姓名
    - couponName: 优惠券名称
    - grantedTimeEnd: 派发时间止区(yyyy-MM-dd)
    - grantedTimeStart: 派发时间起区(yyyy-MM-dd)
    - handlerCardNo: 经办人卡号
    - handlerMobile: 经办人注册手机号
    - handlerRealName: 经办人姓名
    - id: 活动id
    - orderNo: 订单编号
    - orderWay: 下单方式:1-自购,2-代购
    - pageNum: 当前页
    - pageSize: 每页数量
    - payTimeEnd: 订单支付时间止区(yyyy-MM-dd)
    - payTimeStart: 订单支付时间起区(yyyy-MM-dd)
    - returned: 是否已退货
    - state: 派券状态:0-未派发,1-已派发,2-不派发,3-券不足
    - storeCode: 服务中心编号
    """

    url = "/mgmt/prmt/shoppedGift/exportByBuyer"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
