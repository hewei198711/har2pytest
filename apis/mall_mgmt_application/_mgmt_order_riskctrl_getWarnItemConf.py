import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_getWarnItemConf(headers=headers):
    """
    预警项配置
    /mgmt/order/riskctrl/getWarnItemConf
    """

    url = "/mgmt/order/riskctrl/getWarnItemConf"
    with client.get(url=url, headers=headers) as r:
        return r
