import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_promoCopy_getPromoCopyById(params=params, headers=headers):
    """
    促单词条信息查询
    /mgmt/cms/promoCopy/getPromoCopyById

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/promoCopy/getPromoCopyById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
