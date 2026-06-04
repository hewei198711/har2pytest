import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_banner_update_sort(headers=headers):
    """
    Banner排序
    /mgmt/cms/banner/update/sort
    """

    url = "/mgmt/cms/banner/update/sort"
    with client.post(url=url, headers=headers) as r:
        return r
