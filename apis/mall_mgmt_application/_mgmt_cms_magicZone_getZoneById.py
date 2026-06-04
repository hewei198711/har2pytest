import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicZone_getZoneById(params=params, headers=headers):
    """
    根据id回显魔法专区数据
    /mgmt/cms/magicZone/getZoneById

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/magicZone/getZoneById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
