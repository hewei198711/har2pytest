import os

from util.client import client

data = {
    "commitTimeEnd": "",  # 下单时间结束, 格式为 yyyy-MM-dd
    "commitTimeStart": "",  # 下单时间开始, 格式为 yyyy-MM-dd
    "creatorCard": "",  # 开单人卡号
    "creatorName": "",  # 开单人姓名
    "customerCard": "",  # 顾客卡号
    "customerLuckState": 0,  # 抽奖状态：0未抽奖，1已抽奖
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 顾客手机号
    "customerType": 0,  # 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    "luckyActivityId": 0,  # 抽奖活动id
    "orderNo": "",  # 订单编号
    "orderStatus": 0,  # 订单状态 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "payTimeEnd": "",  # 支付时间结束, 格式为 yyyy-MM-dd
    "payTimeStart": "",  # 支付时间开始, 格式为 yyyy-MM-dd
    "source": 0,  # 下单渠道 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_getLuckActivityOrderList(data=data, headers=headers):
    """
    后台获取抽奖活动订单列表
    /mgmt/prmt/luckyActivity/getLuckActivityOrderList

    参数说明:
    - commitTimeEnd: 下单时间结束, 格式为 yyyy-MM-dd
    - commitTimeStart: 下单时间开始, 格式为 yyyy-MM-dd
    - creatorCard: 开单人卡号
    - creatorName: 开单人姓名
    - customerCard: 顾客卡号
    - customerLuckState: 抽奖状态：0未抽奖，1已抽奖
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - customerType: 顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    - luckyActivityId: 抽奖活动id
    - orderNo: 订单编号
    - orderStatus: 订单状态 1->待支付 2->待发货 3->待收货 4->已取消 5->已退货 98->审核取消 99->已完成
    - payTimeEnd: 支付时间结束, 格式为 yyyy-MM-dd
    - payTimeStart: 支付时间开始, 格式为 yyyy-MM-dd
    - source: 下单渠道 1->WEB商城 2->APP商城 3->小程序商城 4->系统下单 5->商城1.0
    - storeCode: 服务中心编号
    """

    url = "/mgmt/prmt/luckyActivity/getLuckActivityOrderList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
