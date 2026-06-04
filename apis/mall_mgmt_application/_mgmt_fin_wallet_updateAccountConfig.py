import os

from util.client import client

params = {
    "type": 0,  # 配置类型，1：服务费显示开关
    "value": 0,  # 配置值，1：开启，0：关闭
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_updateAccountConfig(params=params, headers=headers):
    """
    服务费显示开关修改
    /mgmt/fin/wallet/updateAccountConfig

    参数说明:
    - type: 配置类型，1：服务费显示开关
    - value: 配置值，1：开启，0：关闭
    """

    url = "/mgmt/fin/wallet/updateAccountConfig"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
