import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_getMemberNameAndCreditAmt(data=data, headers=headers):
    """
    通过卡号获取会员姓名以及当前信用额
    /mgmt/fin/wallet/credit/stages/getMemberNameAndCreditAmt

    参数说明:
    - cardNo: 会员卡号
    """

    url = "/mgmt/fin/wallet/credit/stages/getMemberNameAndCreditAmt"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
