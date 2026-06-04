import os

from util.client import client

data = {
    "payNo": "",  # 支付流水号
    "remark": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_pay_verifyAcct_confirmtob(data=data, headers=headers):
    """
    对公支付确认平账
    /mgmt/pay/verifyAcct/confirmtob

    参数说明:
    - payNo: 支付流水号
    - remark: 备注
    """

    url = "/mgmt/pay/verifyAcct/confirmtob"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
