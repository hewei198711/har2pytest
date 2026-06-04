import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "type": 0,  # 配置类型，1：服务费显示开关
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_getAccountConfig(params=params, headers=headers):
    """
    服务费显示开关日志查询
    /mgmt/fin/wallet/getAccountConfig

    参数说明:
    - pageNum: 页数
    - pageSize: 每页显示数
    - type: 配置类型，1：服务费显示开关
    """

    url = "/mgmt/fin/wallet/getAccountConfig"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
