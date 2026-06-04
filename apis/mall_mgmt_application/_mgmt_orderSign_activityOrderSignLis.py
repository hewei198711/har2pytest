import os

from util.client import client

data = {
    "customerCard": "",  # 顾客卡号
    "customerName": "",  # 顾客姓名
    "customerPhone": "",  # 顾客手机号
    "customerType": 0,  # (顾客身份)顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    "endPayTime": "",  # 签约结束时间
    "isContinue": False,  # 是否续签单 true是 , false否
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "payType": 0,  # (签约方式)付款方式，1->一次性付款 2->分期付款
    "promotionId": "",  # 活动id
    "signStatus": 0,  # 签约状态 1->待签约 2->已签约 3->已履约 4->已解约 5->签约失败 6->续约异常
    "signType": 0,  # 签约类型，1:2.0；2：3.0；3：4.0
    "source": 0,  # 签约平台 1->WEB商城 2->APP商城 3->小程序商城
    "startPayTime": "",  # 签约开始时间
    "storeCode": "",  # (门店编号)服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_activityOrderSignLis(data=data, headers=headers):
    """
    活动中心 > 签约购活动管理 > 签约购活动详情 > 签约情况列表
    /mgmt/orderSign/activityOrderSignLis

    参数说明:
    - customerCard: 顾客卡号
    - customerName: 顾客姓名
    - customerPhone: 顾客手机号
    - customerType: (顾客身份)顾客类型 1->普通顾客 2->优惠顾客 3->云商 4->微店
    - endPayTime: 签约结束时间
    - isContinue: 是否续签单 true是 , false否
    - pageNum: 页数
    - pageSize: 每页显示数
    - payType: (签约方式)付款方式，1->一次性付款 2->分期付款
    - promotionId: 活动id
    - signStatus: 签约状态 1->待签约 2->已签约 3->已履约 4->已解约 5->签约失败 6->续约异常
    - signType: 签约类型，1:2.0；2：3.0；3：4.0
    - source: 签约平台 1->WEB商城 2->APP商城 3->小程序商城
    - startPayTime: 签约开始时间
    - storeCode: (门店编号)服务中心编号
    """

    url = "/mgmt/orderSign/activityOrderSignLis"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
