import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_getPromptTextConf(headers=headers):
    """
    获取商城提示文案配置
    /mgmt/order/riskctrl/getPromptTextConf
    """

    url = "/mgmt/order/riskctrl/getPromptTextConf"
    with client.get(url=url, headers=headers) as r:
        return r
