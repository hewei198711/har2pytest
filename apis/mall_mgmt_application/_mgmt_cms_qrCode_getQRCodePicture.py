import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_qrCode_getQRCodePicture(headers=headers):
    """
    获取企业微信二维码内嵌图片
    /mgmt/cms/qrCode/getQRCodePicture
    """

    url = "/mgmt/cms/qrCode/getQRCodePicture"
    with client.get(url=url, headers=headers) as r:
        return r
