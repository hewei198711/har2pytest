import os

from util.client import client

params = {
    "title": "",  # title
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_importDisableMemberTemplate(params=params, headers=headers):
    """
    导入不可参与活动顾客模板下载
    /mgmt/prmt/importDisableMemberTemplate

    参数说明:
    - title: title
    """

    url = "/mgmt/prmt/importDisableMemberTemplate"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
