import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_libertySale_getIntro(headers=headers):
    """
    获取随心购活动介绍
    /mgmt/prmt/libertySale/getIntro
    """

    url = "/mgmt/prmt/libertySale/getIntro"
    with client.get(url=url, headers=headers) as r:
        return r
