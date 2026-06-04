import os

from util.client import client

data = {
    "bankId": 0,  # 签约银行卡id
    "memberId": "",  # 会员id
    "signPayChannelCode": "",  # 签约付银行渠道 206 工行分期付
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_unSignToCustomerIcbcEpay(data=data, headers=headers):
    """
    管理人员解绑顾客工行分期付银行卡
    /mgmt/fin/wallet/unSignToCustomerIcbcEpay

    参数说明:
    - bankId: 签约银行卡id
    - memberId: 会员id
    - signPayChannelCode: 签约付银行渠道 206 工行分期付
    """

    url = "/mgmt/fin/wallet/unSignToCustomerIcbcEpay"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
