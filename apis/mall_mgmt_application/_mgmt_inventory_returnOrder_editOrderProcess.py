import os

from util.client import client

data = {
    "expressCompany": "",  # 快递公司
    "expressFreightProof": "",  # 快递费用凭证url
    "expressFreightProofName": "",  # 快递费用凭证名称
    "expressNo": "",  # 快递单号
    "orderId": 0,  # 退货单id
    "processRemarks": "",  # 退回处理说明
    "returnType": 0,  # 退回类型 1自带 2邮寄
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_returnOrder_editOrderProcess(data=data, headers=headers):
    """
    修改退货单退回处理信息
    /mgmt/inventory/returnOrder/editOrderProcess

    参数说明:
    - expressCompany: 快递公司
    - expressFreightProof: 快递费用凭证url
    - expressFreightProofName: 快递费用凭证名称
    - expressNo: 快递单号
    - orderId: 退货单id
    - processRemarks: 退回处理说明
    - returnType: 退回类型 1自带 2邮寄
    """

    url = "/mgmt/inventory/returnOrder/editOrderProcess"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
