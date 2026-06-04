import os

from util.client import client

data = {
    "configStatus": 0,  # 配置状态:0-全部关闭 1-部分开启 2-全部开启
    "id": 0,  # 主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_setCompanyConfig(data=data, headers=headers):
    """
    设置企业电子发票开关配置
    /mgmt/sys/setCompanyConfig

    参数说明:
    - configStatus: 配置状态:0-全部关闭 1-部分开启 2-全部开启
    - id: 主键id
    """

    url = "/mgmt/sys/setCompanyConfig"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
