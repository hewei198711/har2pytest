import os

from util.client import client

params = {
    "id": 0,  # id
    "status": 0,  # 状态
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_alterPaymentPermission(params=params, headers=headers):
    """
    启用或禁用支付方式
    /mgmt/sys/alterPaymentPermission

    参数说明:
    - id: id
    - status: 状态
    """

    url = "/mgmt/sys/alterPaymentPermission"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
