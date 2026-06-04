import os

from util.client import client

params = {
    "auditStatus": 0,  # 审核状态 1待审核 2已通过 3已驳回
    "companyCode": "",  # 分公司编号
    "companyCodes": [],  # 分公司编号(列表)
    "createBegin": "",  # 下单开始时间
    "createEnd": "",  # 下单结束时间
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "principalCardNo": "",  # 负责人会员(顾客)卡号
    "principalName": "",  # 服务中心负责人(顾客)姓名
    "principalPhone": "",  # 负责人会员(顾客)手机
    "state": 0,  # 团购单状态 1待分公司审核 2待总公司审核 3待发货  4待收货  5已完成 6审核不通过 7取消 8待退票
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_group_order_invoice_audit_page(params=params, headers=headers):
    """
    发票审核列表
    /mgmt/inventory/group-order/invoice/audit/page

    参数说明:
    - auditStatus: 审核状态 1待审核 2已通过 3已驳回
    - companyCode: 分公司编号
    - companyCodes: 分公司编号(列表)
    - createBegin: 下单开始时间
    - createEnd: 下单结束时间
    - orderNo: 订单编号
    - pageNum: 页数
    - pageSize: 页大小
    - principalCardNo: 负责人会员(顾客)卡号
    - principalName: 服务中心负责人(顾客)姓名
    - principalPhone: 负责人会员(顾客)手机
    - state: 团购单状态 1待分公司审核 2待总公司审核 3待发货  4待收货  5已完成 6审核不通过 7取消 8待退票
    """

    url = "/mgmt/inventory/group-order/invoice/audit/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
