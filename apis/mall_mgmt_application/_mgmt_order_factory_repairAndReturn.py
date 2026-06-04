import os

from util.client import client

data = {
    "attachmentList": [],  # 附件列表(回寄快递凭证)
    "consignee": "",  # 完美回寄的收货人
    "consigneeAddress": "",  # 收货人地址
    "consigneeNumber": "",  # 完美回寄的收货人联系电话
    "id": 0,  # 返修单ID
    "isPay": 0,  # 是否已付费：1->是；0->否
    "payRemark": "",  # 付款备注
    "sendExpressName": "",  # 完美回寄的物流公司
    "sendExpressNo": "",  # 完美回寄的运单号
    "sendRemark": "",  # 完美回寄的备注
    "systemCode": 0,  # 查询系统编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_factory_repairAndReturn(data=data, headers=headers):
    """
    执行维修回寄
    /mgmt/order/factory/repairAndReturn

    参数说明:
    - attachmentList: 附件列表(回寄快递凭证)
    - consignee: 完美回寄的收货人
    - consigneeAddress: 收货人地址
    - consigneeNumber: 完美回寄的收货人联系电话
    - id: 返修单ID
    - isPay: 是否已付费：1->是；0->否
    - payRemark: 付款备注
    - sendExpressName: 完美回寄的物流公司
    - sendExpressNo: 完美回寄的运单号
    - sendRemark: 完美回寄的备注
    - systemCode: 查询系统编码
    """

    url = "/mgmt/order/factory/repairAndReturn"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
