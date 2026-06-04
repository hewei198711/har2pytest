import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_getCardNoByStoreCode(params=params, headers=headers):
    """
    根据服务中心编号获取会员卡号
    /mgmt/fin/wallet/getCardNoByStoreCode

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/fin/wallet/getCardNoByStoreCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
