import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_promoCopy_getPromoCopyList(headers=headers):
    """
    促单词条列表查询
    /mgmt/cms/promoCopy/getPromoCopyList
    """

    url = "/mgmt/cms/promoCopy/getPromoCopyList"
    with client.get(url=url, headers=headers) as r:
        return r
