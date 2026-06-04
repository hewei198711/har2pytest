import os
from urllib.parse import urlencode

from util.client import client

data = {
    "autoMonth": 0,  # autoMonth
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_weshop_updateWechatShopOrderConfig(data=data, headers=headers):
    """
    修改微信小店超时配置
    /mgmt/weshop/updateWechatShopOrderConfig

    参数说明:
    - autoMonth: autoMonth
    """

    url = "/mgmt/weshop/updateWechatShopOrderConfig"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
