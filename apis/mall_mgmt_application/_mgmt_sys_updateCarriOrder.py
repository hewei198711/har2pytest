import os

from util.client import client

params = {
    "carriage": "",  # 所需运费，非负数
    "id": "",  # 当前页码,默认为1
    "orderAmount": "",  # 订单金额,为正数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_updateCarriOrder(params=params, headers=headers):
    """
    更新订单收取的费用
    /mgmt/sys/updateCarriOrder

    参数说明:
    - carriage: 所需运费，非负数
    - id: 当前页码,默认为1
    - orderAmount: 订单金额,为正数
    """

    url = "/mgmt/sys/updateCarriOrder"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
