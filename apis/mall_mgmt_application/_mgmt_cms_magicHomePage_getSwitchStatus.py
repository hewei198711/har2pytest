import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_getSwitchStatus(headers=headers):
    """
    获取置灰开关状态
    /mgmt/cms/magicHomePage/getSwitchStatus
    """

    url = "/mgmt/cms/magicHomePage/getSwitchStatus"
    with client.get(url=url, headers=headers) as r:
        return r
