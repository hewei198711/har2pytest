import os

from util.client import client

data = {
    "creditExeDate": 0,  # 每月扣款日期
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_setCreditStagesExeDate(data=data, headers=headers):
    """
    设置扣减日期
    /mgmt/fin/wallet/credit/stages/setCreditStagesExeDate

    参数说明:
    - creditExeDate: 每月扣款日期
    """

    url = "/mgmt/fin/wallet/credit/stages/setCreditStagesExeDate"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
