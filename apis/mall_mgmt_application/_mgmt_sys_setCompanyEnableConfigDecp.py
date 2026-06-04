import os

from util.client import client

data = {
    "enableStatus": False,  # 状态: false-禁用, true-启用
    "id": 0,  # 主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_setCompanyEnableConfigDecp(data=data, headers=headers):
    """
    启用、禁用 数字人名币
    /mgmt/sys/setCompanyEnableConfigDecp

    参数说明:
    - enableStatus: 状态: false-禁用, true-启用
    - id: 主键id
    """

    url = "/mgmt/sys/setCompanyEnableConfigDecp"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
