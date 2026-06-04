import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_pay_method_list(headers=headers):
    """
    从数据字典中获取支付方式
    /mgmt/sys/pay/method/list
    """

    url = "/mgmt/sys/pay/method/list"
    with client.get(url=url, headers=headers) as r:
        return r
