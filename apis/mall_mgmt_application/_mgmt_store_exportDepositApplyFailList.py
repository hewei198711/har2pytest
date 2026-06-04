import os

from util.client import client

params = {
    "importId": "",  # importId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportDepositApplyFailList(params=params, headers=headers):
    """
    批量导入保证金申请失败记录导出
    /mgmt/store/exportDepositApplyFailList

    参数说明:
    - importId: importId
    """

    url = "/mgmt/store/exportDepositApplyFailList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
