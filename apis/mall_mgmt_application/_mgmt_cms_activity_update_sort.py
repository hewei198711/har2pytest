import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_activity_update_sort(headers=headers):
    """
    活动专区排序
    /mgmt/cms/activity/update/sort
    """

    url = "/mgmt/cms/activity/update/sort"
    with client.post(url=url, headers=headers) as r:
        return r
