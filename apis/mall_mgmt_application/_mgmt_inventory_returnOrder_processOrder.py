import os

from util.client import client

data = {
    "expressCompany": "",  # 物流公司
    "expressFreightProof": "",  # 物流费用凭证url
    "expressFreightProofName": "",  # 物流费用凭证名称
    "expressNo": "",  # 物流单号
    "orderId": 0,  # 退货单id
    "processRemarks": "",  # 退回处理说明
    "returnType": 0,  # 退回类型 1自带 2邮寄
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_returnOrder_processOrder(data=data, headers=headers):
    """
    后台押货退货退回处理
    /mgmt/inventory/returnOrder/processOrder

    参数说明:
    - expressCompany: 物流公司
    - expressFreightProof: 物流费用凭证url
    - expressFreightProofName: 物流费用凭证名称
    - expressNo: 物流单号
    - orderId: 退货单id
    - processRemarks: 退回处理说明
    - returnType: 退回类型 1自带 2邮寄
    """

    url = "/mgmt/inventory/returnOrder/processOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
