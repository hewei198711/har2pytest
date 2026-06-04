import os

from util.client import client

data = {
    "auditRemark": "",  # 审批意见
    "id": 0,  # 主键id
    "warnStatus": 0,  # 审批结果，3：同意；4：不同意
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_auditByOrder(data=data, headers=headers):
    """
    订单维度预警报表审批
    /mgmt/order/riskctrl/auditByOrder

    参数说明:
    - auditRemark: 审批意见
    - id: 主键id
    - warnStatus: 审批结果，3：同意；4：不同意
    """

    url = "/mgmt/order/riskctrl/auditByOrder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
