import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_advert_getAdvertList(headers=headers):
    """
    广告页列表
    /mgmt/cms/advert/getAdvertList
    """

    url = "/mgmt/cms/advert/getAdvertList"
    with client.get(url=url, headers=headers) as r:
        return r
