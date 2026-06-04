import os

from util.client import client

data = {
    "attachmentUrlList": [],  # 退货凭证URL列表
    "reason1": "",  # 一级退货原因
    "reason1Id": 0,  # 一级退货原因id
    "reason1Remark": "",  # 一级退货原因备注
    "reason2": "",  # 二级退货原因
    "reason2Id": 0,  # 二级退货原因id
    "reason2Remark": "",  # 二级退货原因备注
    "returnNo": "",  # 退货单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_updateOrderReturn(data=data, headers=headers):
    """
    修改退货申请
    /mgmt/order/return/updateOrderReturn

    参数说明:
    - attachmentUrlList: 退货凭证URL列表
    - reason1: 一级退货原因
    - reason1Id: 一级退货原因id
    - reason1Remark: 一级退货原因备注
    - reason2: 二级退货原因
    - reason2Id: 二级退货原因id
    - reason2Remark: 二级退货原因备注
    - returnNo: 退货单号
    """

    url = "/mgmt/order/return/updateOrderReturn"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
