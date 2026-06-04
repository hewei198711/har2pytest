import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_giftPromotion_getPostQrCode(headers=headers):
    """
    获取收礼分享海报二维码
    /mgmt/cms/giftPromotion/getPostQrCode
    """

    url = "/mgmt/cms/giftPromotion/getPostQrCode"
    with client.get(url=url, headers=headers) as r:
        return r
