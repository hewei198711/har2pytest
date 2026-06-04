import os

from util.client import client

params = {
    "type": 0,  # 配置类型，1：服务费显示开关
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_getAccountConfigValue(params=params, headers=headers):
    """
    服务费显示开关查询，返回1：开启，0：关闭，默认关闭
    /mgmt/fin/wallet/getAccountConfigValue

    参数说明:
    - type: 配置类型，1：服务费显示开关
    """

    url = "/mgmt/fin/wallet/getAccountConfigValue"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
