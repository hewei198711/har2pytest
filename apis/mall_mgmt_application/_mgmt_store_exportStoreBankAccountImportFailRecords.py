import os

from util.client import client

params = {
    "failResultKey": "",  # 失败记录的key
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportStoreBankAccountImportFailRecords(params=params, headers=headers):
    """
    导出店铺银行账号导入失败记录
    /mgmt/store/exportStoreBankAccountImportFailRecords

    参数说明:
    - failResultKey: 失败记录的key
    """

    url = "/mgmt/store/exportStoreBankAccountImportFailRecords"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
