import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_wallet_credit_stages_queryCreditStagesExeDateData(headers=headers):
    """
    信用分期付扣款日期查询
    /mgmt/fin/wallet/credit/stages/queryCreditStagesExeDateData
    """

    url = "/mgmt/fin/wallet/credit/stages/queryCreditStagesExeDateData"
    with client.post(url=url, headers=headers) as r:
        return r
