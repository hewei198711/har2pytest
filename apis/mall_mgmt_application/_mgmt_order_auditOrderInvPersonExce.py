import os

from util.client import client

data = {
    "auditRemark": "",  # 审核备注
    "auditStatus": 0,  # 审核状态 2->已通过 3->已驳回
    "ids": [],  # id集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_auditOrderInvPersonExce(data=data, headers=headers):
    """
    审核异常个人要票订单
    /mgmt/order/auditOrderInvPersonExce

    参数说明:
    - auditRemark: 审核备注
    - auditStatus: 审核状态 2->已通过 3->已驳回
    - ids: id集合
    """

    url = "/mgmt/order/auditOrderInvPersonExce"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
