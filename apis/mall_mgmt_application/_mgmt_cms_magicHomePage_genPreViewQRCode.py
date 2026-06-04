import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_genPreViewQRCode(params=params, headers=headers):
    """
    生成魔法首页预览二维码
    /mgmt/cms/magicHomePage/genPreViewQRCode

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/magicHomePage/genPreViewQRCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
