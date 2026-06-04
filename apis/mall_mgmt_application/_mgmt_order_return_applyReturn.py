import os

from util.client import client

data = {
    "applySource": 0,  # 来源 0->总公司代客申请 1->顾客申请 2->公司申请
    "attachmentUrlList": [],  # 退货凭证URL列表
    "orderNo": "",  # 订单编号
    "reason1": "",  # 退货一级原因
    "reason1Id": 0,  # 退货一级原因id
    "reason1Remark": "",  # 退货一级原因备注
    "reason2": "",  # 退货二级原因
    "reason2Id": 0,  # 退货二级原因id
    "reason2Remark": "",  # 退货二级原因备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_applyReturn(data=data, headers=headers):
    """
    申请退货
    /mgmt/order/return/applyReturn

    参数说明:
    - applySource: 来源 0->总公司代客申请 1->顾客申请 2->公司申请
    - attachmentUrlList: 退货凭证URL列表
    - orderNo: 订单编号
    - reason1: 退货一级原因
    - reason1Id: 退货一级原因id
    - reason1Remark: 退货一级原因备注
    - reason2: 退货二级原因
    - reason2Id: 退货二级原因id
    - reason2Remark: 退货二级原因备注
    """

    url = "/mgmt/order/return/applyReturn"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
