import os

from util.client import client

params = {
    "applyTimeBegin": "",  # 申请开始时间 #格式yyyy-MM-dd
    "applyTimeEnd": "",  # 申请结束时间 #格式yyyy-MM-dd
    "customerCard": "",  # 顾客卡号
    "customerPhone": "",  # 顾客手机号
    "orderNo": "",  # 订单号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "returnNo": "",  # 退货单号
    "returnStatus": 0,  # 服务状态  1->待审核 2->待退回 3->待验货 98->已取消 99->已完成
    "returnType": 0,  # 退货类型 1->当月退货 2->隔月退货
    "tabType": 0,  # 店交付 1->店交付 2->顾客自购店交付；不传就默认全部
    "waitAuditType": 0,  # 待审核类型  1->待服务中心审核 2->待分公司审核
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_orderReturn_list(params=params, headers=headers):
    """
    售后列表
    /appStore/orderReturn/list

    参数说明:
    - applyTimeBegin: 申请开始时间 #格式yyyy-MM-dd
    - applyTimeEnd: 申请结束时间 #格式yyyy-MM-dd
    - customerCard: 顾客卡号
    - customerPhone: 顾客手机号
    - orderNo: 订单号
    - pageNum: 页数
    - pageSize: 每页显示数
    - returnNo: 退货单号
    - returnStatus: 服务状态  1->待审核 2->待退回 3->待验货 98->已取消 99->已完成
    - returnType: 退货类型 1->当月退货 2->隔月退货
    - tabType: 店交付 1->店交付 2->顾客自购店交付；不传就默认全部
    - waitAuditType: 待审核类型  1->待服务中心审核 2->待分公司审核
    """

    url = "/appStore/orderReturn/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
