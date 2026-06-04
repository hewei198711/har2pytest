import os

from util.client import client

data = {
    "orderNo": None,  # 兑换流水号
    "exchangeType": None,  # 兑换产品类型 1-优惠券,2-实物物品,3-油葱学堂课程,4-会议室,5体验中心兑换品
    "customerPhone": None,  # 顾客手机号
    "customerCard": None,  # 顾客卡号
    "customerName": None,  # 顾客姓名
    "batchOrderNo": None,  # 批量兑换单号
    "creatorCard": None,  # 开单人卡号
    "orderStatus": None,  # 订单状态 1->待支付 2->待发货 3->待收货(已发货) 4->已取消 5->已退货 6->待核销 99->已完成
    "pageNum": 1,  # TODO: 添加参数说明
    "pageSize": 10,  # TODO: 添加参数说明
    "hxTimeBegin": None,  # 核销时间-开始
    "hxTimeEnd": None,  # 核销时间-结束
    "exchangeTimeBegin": None,  # 兑换时间-开始
    "exchangeTimeEnd": None,  # 兑换时间-结束
}

headers = {
    "channel": "pc",
    "client": "store",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _user_order_getStoreAgentOrderList(data=data, headers=headers):
    """
    PC店铺查询兑换订单列表
    /user/order/getStoreAgentOrderList

    参数说明:
    - batchOrderNo: 批量兑换单号
    - creatorCard: 开单人卡号
    - customerCard: 顾客卡号
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - exchangeNoWord: 兑换品编码/名称
    - exchangeTimeBegin: 兑换时间-开始
    - exchangeTimeEnd: 兑换时间-结束
    - exchangeType: 兑换产品类型 1-优惠券,2-实物物品,3-油葱学堂课程,4-会议室,5体验中心兑换品
    - hxTimeBegin: 核销时间-开始
    - hxTimeEnd: 核销时间-结束
    - orderNo: 兑换流水号
    - orderStatus: 订单状态 1->待支付 2->待发货 3->待收货(已发货) 4->已取消 5->已退货 6->待核销 99->已完成
    """

    url = "/user/order/getStoreAgentOrderList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
