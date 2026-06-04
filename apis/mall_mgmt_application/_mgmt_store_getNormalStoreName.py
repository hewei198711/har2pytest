import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getNormalStoreName(params=params, headers=headers):
    """
    返回权限不为取消资格的服务中心名称
    /mgmt/store/getNormalStoreName

    参数说明:
    - storeCode: 服务中心编码
    """

    url = "/mgmt/store/getNormalStoreName"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
