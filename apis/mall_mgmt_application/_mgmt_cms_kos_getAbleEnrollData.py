import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_getAbleEnrollData(headers=headers):
    """
    数据看板-可报名数据
    /mgmt/cms/kos/getAbleEnrollData
    """

    url = "/mgmt/cms/kos/getAbleEnrollData"
    with client.get(url=url, headers=headers) as r:
        return r
