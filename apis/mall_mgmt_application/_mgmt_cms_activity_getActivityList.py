import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_activity_getActivityList(headers=headers):
    """
    活动列表
    /mgmt/cms/activity/getActivityList
    """

    url = "/mgmt/cms/activity/getActivityList"
    with client.get(url=url, headers=headers) as r:
        return r
