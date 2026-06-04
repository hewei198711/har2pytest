import os

from util.client import client

params = {
    "cardNo": "",  # cardNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_getCreditAmountByCardNo(params=params, headers=headers):
    """
    根据会员卡号获取顾客姓名和现有信用额
    /mgmt/fin/wallet/getCreditAmountByCardNo

    参数说明:
    - cardNo: cardNo
    """

    url = "/mgmt/fin/wallet/getCreditAmountByCardNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
