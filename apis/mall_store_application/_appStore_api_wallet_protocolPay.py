import os

from util.client import client

data = {
    "isFirst": False,  # 是否首单  true： 是    false： 否
    "mortgageOrderNo": "",  # 押货单号
    "payDTO": "",  # 支付主体参数
    "protocolOrderNo": "",  # 签约单号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_api_wallet_protocolPay(data=data, headers=headers):
    """
    签约购支付
    /appStore/api/wallet/protocolPay

    参数说明:
    - isFirst: 是否首单  true： 是    false： 否
    - mortgageOrderNo: 押货单号
    - payDTO: 支付主体参数
    - protocolOrderNo: 签约单号
    """

    url = "/appStore/api/wallet/protocolPay"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
