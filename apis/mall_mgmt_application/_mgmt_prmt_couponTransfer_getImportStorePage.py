import os

from util.client import client

params = {
    "code": "",  # code
    "grantId": 0,  # grantId
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponTransfer_getImportStorePage(params=params, headers=headers):
    """
    分页查询导入门店(导入时)
    /mgmt/prmt/couponTransfer/getImportStorePage

    参数说明:
    - code: code
    - grantId: grantId
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/prmt/couponTransfer/getImportStorePage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
