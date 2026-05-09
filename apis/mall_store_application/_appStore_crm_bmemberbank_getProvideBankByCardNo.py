import os

from util.client import client

params = {
    "cardNo": "",  # cardNo
    "platform": 0,  # platform
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_crm_bmemberbank_getProvideBankByCardNo(params=params, headers=headers):
    """
    根据会员卡号查询会员发放银行卡信息
    /appStore/crm/bmemberbank/getProvideBankByCardNo

    参数说明:
    - cardNo: cardNo
    - platform: platform
    """

    url = "/appStore/crm/bmemberbank/getProvideBankByCardNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
