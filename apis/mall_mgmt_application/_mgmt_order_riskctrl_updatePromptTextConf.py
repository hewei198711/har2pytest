import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "promptText": "",  # 商城提示文案
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_updatePromptTextConf(data=data, headers=headers):
    """
    修改商城提示文案
    /mgmt/order/riskctrl/updatePromptTextConf

    参数说明:
    - id: 主键id
    - promptText: 商城提示文案
    """

    url = "/mgmt/order/riskctrl/updatePromptTextConf"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
