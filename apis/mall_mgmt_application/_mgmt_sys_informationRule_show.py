import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_informationRule_show(headers=headers):
    """
    法规咨询-展示
    /mgmt/sys/informationRule/show
    """

    url = "/mgmt/sys/informationRule/show"
    with client.get(url=url, headers=headers) as r:
        return r
