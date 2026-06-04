import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_ecenter_getExperienceCenterList(headers=headers):
    """
    体验中心列表
    /mgmt/ecenter/getExperienceCenterList
    """

    url = "/mgmt/ecenter/getExperienceCenterList"
    with client.get(url=url, headers=headers) as r:
        return r
