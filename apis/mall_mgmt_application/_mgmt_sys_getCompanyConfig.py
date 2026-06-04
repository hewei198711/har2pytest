import os

from util.client import client

params = {
    "configType": "",  # 配置类型:1-企业电子发票 2-数字人名币
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getCompanyConfig(params=params, headers=headers):
    """
    获取企业电子发票/数字人名币开关配置
    /mgmt/sys/getCompanyConfig

    参数说明:
    - configType: 配置类型:1-企业电子发票 2-数字人名币
    """

    url = "/mgmt/sys/getCompanyConfig"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
