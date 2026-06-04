import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_exportBatchdtlMessage(headers=headers):
    """
    信用额调整批次详情-导出错误信息
    /mgmt/fin/wallet/credit/exportBatchdtlMessage
    """

    url = "/mgmt/fin/wallet/credit/exportBatchdtlMessage"
    with client.get(url=url, headers=headers) as r:
        return r
