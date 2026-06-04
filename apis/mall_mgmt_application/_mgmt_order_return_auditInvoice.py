import os

from util.client import client

data = {
    "attachmentUrlList": [],  # 审核附件URL列表
    "auditStatus": 0,  # 审核状态  1->通过 2->不通过
    "remarks": "",  # 审核意见
    "serviceNo": "",  # 售后单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_auditInvoice(data=data, headers=headers):
    """
    退票审核
    /mgmt/order/return/auditInvoice

    参数说明:
    - attachmentUrlList: 审核附件URL列表
    - auditStatus: 审核状态  1->通过 2->不通过
    - remarks: 审核意见
    - serviceNo: 售后单号
    """

    url = "/mgmt/order/return/auditInvoice"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
