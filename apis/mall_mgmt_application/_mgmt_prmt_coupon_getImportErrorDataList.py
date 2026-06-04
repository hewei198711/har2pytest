import os

from util.client import client

params = {
    "key": "",  # key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_getImportErrorDataList(params=params, headers=headers):
    """
    查询导入错误商品列表
    /mgmt/prmt/coupon/getImportErrorDataList

    参数说明:
    - key: key
    """

    url = "/mgmt/prmt/coupon/getImportErrorDataList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
