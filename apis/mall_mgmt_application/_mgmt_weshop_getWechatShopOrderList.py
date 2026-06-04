import os

from util.client import client

data = {
    "channelsName": "",  # 视频号名字
    "customerCardNo": "",  # 顾客卡号
    "customerMobile": "",  # 顾客注册手机号
    "customerName": "",  # 顾客姓名
    "customerTypeList": [],  # 顾客类型，1->普通顾客；2->优惠顾客；3->云商；4->微店；0->未知
    "from": 0,  # TODO: 添加参数说明
    "hasUnknown": False,  # TODO: 添加参数说明
    "memberCardNo": "",  # 会员卡号
    "memberMobile": "",  # 会员注册手机号
    "memberName": "",  # 会员姓名
    "orderEndTime": "",  # 下单结束时间，格式yyyy-MM-dd
    "orderId": "",  # 订单号
    "orderStartTime": "",  # 下单开始时间，格式yyyy-MM-dd
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "receiverMobile": "",  # 收货人手机号
    "receiverName": "",  # 收货人姓名
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_weshop_getWechatShopOrderList(data=data, headers=headers):
    """
    订单管理-微信小店订单列表
    /mgmt/weshop/getWechatShopOrderList

    参数说明:
    - channelsName: 视频号名字
    - customerCardNo: 顾客卡号
    - customerMobile: 顾客注册手机号
    - customerName: 顾客姓名
    - customerTypeList: 顾客类型，1->普通顾客；2->优惠顾客；3->云商；4->微店；0->未知
    - memberCardNo: 会员卡号
    - memberMobile: 会员注册手机号
    - memberName: 会员姓名
    - orderEndTime: 下单结束时间，格式yyyy-MM-dd
    - orderId: 订单号
    - orderStartTime: 下单开始时间，格式yyyy-MM-dd
    - pageNum: 页数
    - pageSize: 每页显示数
    - receiverMobile: 收货人手机号
    - receiverName: 收货人姓名
    - storeCode: 服务中心编号
    """

    url = "/mgmt/weshop/getWechatShopOrderList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
