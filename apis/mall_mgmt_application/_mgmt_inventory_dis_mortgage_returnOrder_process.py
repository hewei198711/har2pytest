import os

from util.client import client

data = {
    "expressCompany": "",  # 物流公司
    "expressNo": "",  # 物流单号
    "expressProofName": "",  # 快递凭证名称
    "expressProofUrl": "",  # 快递凭证url
    "orderId": 0,  # 退货单id
    "processRemark": "",  # 退回处理说明
    "returnType": 0,  # 退回类型 1自带 2邮寄
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_returnOrder_process(data=data, headers=headers):
    """
    退回处理
    /mgmt/inventory/dis/mortgage/returnOrder/process

    参数说明:
    - expressCompany: 物流公司
    - expressNo: 物流单号
    - expressProofName: 快递凭证名称
    - expressProofUrl: 快递凭证url
    - orderId: 退货单id
    - processRemark: 退回处理说明
    - returnType: 退回类型 1自带 2邮寄
    """

    url = "/mgmt/inventory/dis/mortgage/returnOrder/process"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
