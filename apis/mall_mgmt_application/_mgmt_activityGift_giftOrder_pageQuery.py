import os
from util.client import client

data = {
    "commitTimeEnd": "",  # 下单结束时间
    "commitTimeStart": "",  # 下单开始时间
    "giftPromotionId": 0,  # 礼物活动ID
    "orderNo": "",  # 订单号
    "orderStatusList": [],  # 订单状态集合（参考OrderStatus枚举）：
1:待支付, -5:待收礼, 2:待发货, 3:待收货, 99:已完成, 4:已取消, 5:已退款
    "pageNum": 0,  # 分页页码
    "pageSize": 0,  # 分页大小
    "payTimeEnd": "",  # 支付结束时间
    "payTimeStart": "",  # 支付开始时间
    "receiveStatus": 0,  # 收礼状态 0-未收 1-已收
    "receiverCard": "",  # 收礼人卡号
    "receiverName": "",  # 收礼人姓名
    "receiverPhone": "",  # 收礼人手机
    "receiverType": 0,  # 收礼人身份类型 1-普通顾客 2-优惠顾客 3-云商 4-微店
    "senderCard": "",  # 送礼人卡号
    "senderName": "",  # 送礼人姓名
    "senderPhone": "",  # 送礼人手机
    "senderType": 0,  # 送礼人身份类型 1-普通顾客 2-优惠顾客 3-云商 4-微店
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}
def _mgmt_activityGift_giftOrder_pageQuery(data=data, headers=headers):
    """
    分页查询礼物订单活动列表
    /mgmt/activityGift/giftOrder/pageQuery

    参数说明:
    - commitTimeEnd: 下单结束时间
    - commitTimeStart: 下单开始时间
    - giftPromotionId: 礼物活动ID
    - orderNo: 订单号
    - orderStatusList: 订单状态集合（参考OrderStatus枚举）：
1:待支付, -5:待收礼, 2:待发货, 3:待收货, 99:已完成, 4:已取消, 5:已退款
    - pageNum: 分页页码
    - pageSize: 分页大小
    - payTimeEnd: 支付结束时间
    - payTimeStart: 支付开始时间
    - receiveStatus: 收礼状态 0-未收 1-已收
    - receiverCard: 收礼人卡号
    - receiverName: 收礼人姓名
    - receiverPhone: 收礼人手机
    - receiverType: 收礼人身份类型 1-普通顾客 2-优惠顾客 3-云商 4-微店
    - senderCard: 送礼人卡号
    - senderName: 送礼人姓名
    - senderPhone: 送礼人手机
    - senderType: 送礼人身份类型 1-普通顾客 2-优惠顾客 3-云商 4-微店
    """

    url = "/mgmt/activityGift/giftOrder/pageQuery"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
