import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_exportCreditApplyErrorMsg(headers=headers):
    """
    顾客信用额列表-导出错误信息
    /mgmt/fin/wallet/credit/exportCreditApplyErrorMsg
    """

    url = "/mgmt/fin/wallet/credit/exportCreditApplyErrorMsg"
    with client.get(url=url, headers=headers) as r:
        return r
