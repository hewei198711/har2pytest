import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_banner_sort(headers=headers):
    """
    轮播图排序
    /mgmt/acc/banner/sort
    """

    url = "/mgmt/acc/banner/sort"
    with client.post(url=url, headers=headers) as r:
        return r
