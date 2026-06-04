import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicZone_genPcPreViewUrl(params=params, headers=headers):
    """
    生成魔法专区PC预览链接
    /mgmt/cms/magicZone/genPcPreViewUrl

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/magicZone/genPcPreViewUrl"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
