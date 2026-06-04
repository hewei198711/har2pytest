import os

from util.client import client

data = {
    "confType": 0,  # 配置类型（前端不用传）
    "confValue": "",  # 秒返券/电子礼券说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_updateGiftCouponExplain(data=data, headers=headers):
    """
    修改电子礼券说明
    /mgmt/fin/wallet/updateGiftCouponExplain

    参数说明:
    - confType: 配置类型（前端不用传）
    - confValue: 秒返券/电子礼券说明
    """

    url = "/mgmt/fin/wallet/updateGiftCouponExplain"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
