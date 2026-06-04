import os

from util.client import client

data = {
    "id": 0,  # id
    "status": 0,  # 状态
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_pay_method_status_update(data=data, headers=headers):
    """
    修改数据字典中的支付方式的状态
    /mgmt/sys/pay/method/status/update

    参数说明:
    - id: id
    - status: 状态
    """

    url = "/mgmt/sys/pay/method/status/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
