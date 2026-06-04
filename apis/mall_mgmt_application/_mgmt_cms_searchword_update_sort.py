import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_searchword_update_sort(headers=headers):
    """
    热词排序
    /mgmt/cms/searchword/update/sort
    """

    url = "/mgmt/cms/searchword/update/sort"
    with client.post(url=url, headers=headers) as r:
        return r
