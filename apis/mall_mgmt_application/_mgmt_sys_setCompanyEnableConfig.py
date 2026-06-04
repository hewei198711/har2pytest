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


def _mgmt_sys_setCompanyEnableConfig(data=data, headers=headers):
    """
    启用、禁用 企业电子发票
    /mgmt/sys/setCompanyEnableConfig

    参数说明:
    - enableStatus: 状态: false-禁用, true-启用
    - id: 主键id
    """

    url = "/mgmt/sys/setCompanyEnableConfig"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
