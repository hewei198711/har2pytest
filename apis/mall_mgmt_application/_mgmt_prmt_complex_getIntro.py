import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_complex_getIntro(headers=headers):
    """
    获取签约购活动介绍
    /mgmt/prmt/complex/getIntro
    """

    url = "/mgmt/prmt/complex/getIntro"
    with client.get(url=url, headers=headers) as r:
        return r
