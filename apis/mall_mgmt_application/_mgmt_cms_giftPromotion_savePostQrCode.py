import os

from util.client import client

data = {
    "qrCodeUrl": "",  # 海报二维码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_giftPromotion_savePostQrCode(data=data, headers=headers):
    """
    保存收礼分享海报二维码
    /mgmt/cms/giftPromotion/savePostQrCode

    参数说明:
    - qrCodeUrl: 海报二维码
    """

    url = "/mgmt/cms/giftPromotion/savePostQrCode"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
