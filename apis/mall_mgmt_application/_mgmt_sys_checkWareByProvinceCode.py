import os

from util.client import client

params = {
    "provinceCode": "",  # 省份编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_checkWareByProvinceCode(params=params, headers=headers):
    """
    查询所在地是否存在可用仓库
    /mgmt/sys/checkWareByProvinceCode

    参数说明:
    - provinceCode: 省份编码
    """

    url = "/mgmt/sys/checkWareByProvinceCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
