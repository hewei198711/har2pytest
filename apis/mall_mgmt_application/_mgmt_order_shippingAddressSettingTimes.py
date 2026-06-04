import os
from urllib.parse import urlencode

from util.client import client

data = {
    "times": "",  # times
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_shippingAddressSettingTimes(data=data, headers=headers):
    """
    订单管理-修改收货地址记录-设置修改次数
    /mgmt/order/shippingAddressSettingTimes

    参数说明:
    - times: times
    """

    url = "/mgmt/order/shippingAddressSettingTimes"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
