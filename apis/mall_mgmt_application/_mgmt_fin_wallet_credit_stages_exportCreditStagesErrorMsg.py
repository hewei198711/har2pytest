import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_exportCreditStagesErrorMsg(headers=headers):
    """
    信用额分期管理批量导出失败记录
    /mgmt/fin/wallet/credit/stages/exportCreditStagesErrorMsg
    """

    url = "/mgmt/fin/wallet/credit/stages/exportCreditStagesErrorMsg"
    with client.get(url=url, headers=headers) as r:
        return r
