import os

from util.client import client

data = {
    "orderNo": "EX914008260407000001",  # 兑换流水号
    "customerPhone": None,  # 顾客手机号
    "customerCard": None,  # 顾客卡号
    "creatorCard": None,  # 开单人卡号
    "exchangeNoWord": None,  # 兑换品编码/名称
    "customerType": None,  # 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店 5->云+子账号
    "expressType": None,  # 配送方式 1->服务中心自提 2->公司配送
    "orderWay": None,  # 下单方式 1->自购订单 2->代购订单
    "customerSource": None,  # 顾客来源平台:0->商城mall；1->健康health；2->学堂edu；4->荟友趣
    "exchangeTimeBegin": None,  # 兑换时间-开始
    "exchangeTimeEnd": None,  # 兑换时间-结束
    "pageNum": 1,  # TODO: 添加参数说明
    "pageSize": 10,  # TODO: 添加参数说明
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _user_mgmt_order_return_queryOrder(data=data, headers=headers):
    """
    分页查询代客售后订单管理列表
    /user/mgmt/order/return/queryOrder

    参数说明:
    - req: req
    - creatorCard: 开单人卡号
    - customerCard: 顾客卡号
    - customerPhone: 顾客手机号
    - customerSource: 顾客来源平台:0->商城mall；1->健康health；2->学堂edu；4->荟友趣
    - customerType: 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店 5->云+子账号
    - exchangeNoWord: 兑换品编码/名称
    - exchangeTimeBegin: 兑换时间-开始
    - exchangeTimeEnd: 兑换时间-结束
    - expressType: 配送方式 1->服务中心自提 2->公司配送
    - orderNo: 兑换流水号
    - orderWay: 下单方式 1->自购订单 2->代购订单
    """

    url = "/user/mgmt/order/return/queryOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
