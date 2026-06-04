import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_iconSetting_updateIcon_sort(headers=headers):
    """
    icon排序
    /mgmt/cms/iconSetting/updateIcon/sort
    """

    url = "/mgmt/cms/iconSetting/updateIcon/sort"
    with client.post(url=url, headers=headers) as r:
        return r
