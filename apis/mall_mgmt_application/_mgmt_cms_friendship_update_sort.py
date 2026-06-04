import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_friendship_update_sort(headers=headers):
    """
    友情链接排序
    /mgmt/cms/friendship/update/sort
    """

    url = "/mgmt/cms/friendship/update/sort"
    with client.post(url=url, headers=headers) as r:
        return r
