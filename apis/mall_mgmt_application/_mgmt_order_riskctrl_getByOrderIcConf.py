import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_order_riskctrl_getByOrderIcConf(headers=headers):
    """
    获取订单维度预警报表拦截配置
    /mgmt/order/riskctrl/getByOrderIcConf
    """

    url = "/mgmt/order/riskctrl/getByOrderIcConf"
    with client.post(url=url, headers=headers) as r:
        return r
