import os

from util.client import client

data = {
    "pictUrl": "",  # 内嵌图片url
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_qrCode_saveQRCodePicture(data=data, headers=headers):
    """
    保存企业微信二维码内嵌图片
    /mgmt/cms/qrCode/saveQRCodePicture

    参数说明:
    - pictUrl: 内嵌图片url
    """

    url = "/mgmt/cms/qrCode/saveQRCodePicture"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
