import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicZone_genPreViewQRCode(params=params, headers=headers):
    """
    生成魔法专区预览二维码
    /mgmt/cms/magicZone/genPreViewQRCode

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/magicZone/genPreViewQRCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
