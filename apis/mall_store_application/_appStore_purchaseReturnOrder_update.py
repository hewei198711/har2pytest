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


def _appStore_purchaseReturnOrder_update(data=data, headers=headers):
    """
    退货单退回信息修改
    /appStore/purchaseReturnOrder/update

    参数说明:
    - expressCompany: 快递公司
    - expressFreightProof: 快递费用凭证url
    - expressFreightProofName: 快递费用凭证名称
    - expressNo: 快递单号
    - orderId: 退货单id
    - processRemarks: 退回处理说明
    - returnType: 退回类型 1自带 2邮寄
    """

    url = "/appStore/purchaseReturnOrder/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
