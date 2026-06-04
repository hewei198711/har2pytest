import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_exportBatchDetailErrorMsg(headers=headers):
    """
    云商信用额录入批次详情列表批量导入-导出错误信息
    /mgmt/fin/wallet/credit/exportBatchDetailErrorMsg
    """

    url = "/mgmt/fin/wallet/credit/exportBatchDetailErrorMsg"
    with client.get(url=url, headers=headers) as r:
        return r
