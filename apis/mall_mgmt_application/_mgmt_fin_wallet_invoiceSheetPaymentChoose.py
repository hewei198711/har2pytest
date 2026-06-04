import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_invoiceSheetPaymentChoose(headers=headers):
    """
    计算表.选择付款单位
    /mgmt/fin/wallet/invoiceSheetPaymentChoose
    """

    url = "/mgmt/fin/wallet/invoiceSheetPaymentChoose"
    with client.get(url=url, headers=headers) as r:
        return r
