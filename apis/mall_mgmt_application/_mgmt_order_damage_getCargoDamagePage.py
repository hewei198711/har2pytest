import os

from util.client import client

params = {
    "applyTimeBegin": "",  # 申请开始时间 #格式yyyy-MM-dd
    "applyTimeEnd": "",  # 申请结束时间 #格式yyyy-MM-dd
    "companyCode": "",  # 业务分公司编码
    "companyName": "",  # 业务分公司名称
    "creatorCard": "",  # 开单人卡号
    "customerCard": "",  # 顾客卡号
    "damageNo": "",  # 货损货差号
    "damageStatus": 0,  # 状态 1->待审核 2->待发货 3->待收货 99->已完成 98->已取消
    "damageType": 0,  # 货损货差类型 1货损 2货差
    "from": 0,  # TODO: 添加参数说明
    "orderNo": "",  # 订单号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "source": 0,  # 申请端口 : 1=油葱商城 ,2=运营后台
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_damage_getCargoDamagePage(params=params, headers=headers):
    """
    货损货差列表（分页）
    /mgmt/order/damage/getCargoDamagePage

    参数说明:
    - applyTimeBegin: 申请开始时间 #格式yyyy-MM-dd
    - applyTimeEnd: 申请结束时间 #格式yyyy-MM-dd
    - companyCode: 业务分公司编码
    - companyName: 业务分公司名称
    - creatorCard: 开单人卡号
    - customerCard: 顾客卡号
    - damageNo: 货损货差号
    - damageStatus: 状态 1->待审核 2->待发货 3->待收货 99->已完成 98->已取消
    - damageType: 货损货差类型 1货损 2货差
    - orderNo: 订单号
    - pageNum: 页数
    - pageSize: 每页显示数
    - source: 申请端口 : 1=油葱商城 ,2=运营后台
    """

    url = "/mgmt/order/damage/getCargoDamagePage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
