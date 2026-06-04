import os

from util.client import client

params = {
    "id": "",  # 活动id,新增时校验活动编码不传id
    "promotionCode": "",  # 活动编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_sendGift_checkPromotionCodeExists(params=params, headers=headers):
    """
    检验活动编码是否已经存在
    /mgmt/prmt/sendGift/checkPromotionCodeExists

    参数说明:
    - id: 活动id,新增时校验活动编码不传id
    - promotionCode: 活动编码
    """

    url = "/mgmt/prmt/sendGift/checkPromotionCodeExists"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
