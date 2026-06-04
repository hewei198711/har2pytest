import os

from util.client import client

data = {
    "memberId": 0,  # 会员id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_getMemberCreditAmt(data=data, headers=headers):
    """
    通过卡号获取会员姓名以及当前信用额(无检查校验)
    /mgmt/fin/wallet/credit/stages/getMemberCreditAmt

    参数说明:
    - memberId: 会员id
    """

    url = "/mgmt/fin/wallet/credit/stages/getMemberCreditAmt"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
