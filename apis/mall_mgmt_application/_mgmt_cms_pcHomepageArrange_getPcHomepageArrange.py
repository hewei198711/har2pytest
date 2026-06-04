import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_pcHomepageArrange_getPcHomepageArrange(headers=headers):
    """
    获取pc端首页排序
    /mgmt/cms/pcHomepageArrange/getPcHomepageArrange
    """

    url = "/mgmt/cms/pcHomepageArrange/getPcHomepageArrange"
    with client.get(url=url, headers=headers) as r:
        return r
