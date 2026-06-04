import os

from util.client import client

params = {
    "id": 0,  # id
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_listBankAccountLog(params=params, headers=headers):
    """
    银行账号操作记录
    /mgmt/store/listBankAccountLog

    参数说明:
    - id: id
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/store/listBankAccountLog"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
