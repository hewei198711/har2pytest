import os

from util.client import client

data = {
    "eachReduceAmt": 0.0,  # 每期扣减金额
    "memberId": 0,  # 会员id
    "remark": "",  # 调整备注
    "walletId": 0,  # 钱包id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_submitCreditStagesData(data=data, headers=headers):
    """
    信用分期管理提交功能
    /mgmt/fin/wallet/credit/stages/submitCreditStagesData

    参数说明:
    - eachReduceAmt: 每期扣减金额
    - memberId: 会员id
    - remark: 调整备注
    - walletId: 钱包id
    """

    url = "/mgmt/fin/wallet/credit/stages/submitCreditStagesData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
