import os

from util.client import client

params = {
    "key": "",  # 导入操作键
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shelvesCoupon_getImportFailedList(params=params, headers=headers):
    """
    下载导入上架对象失败列表
    /mgmt/prmt/shelvesCoupon/getImportFailedList

    参数说明:
    - key: 导入操作键
    """

    url = "/mgmt/prmt/shelvesCoupon/getImportFailedList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
