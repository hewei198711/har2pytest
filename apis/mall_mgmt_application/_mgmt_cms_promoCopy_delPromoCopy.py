import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_promoCopy_delPromoCopy(data=data, headers=headers):
    """
    促单词条删除接口
    /mgmt/cms/promoCopy/delPromoCopy

    参数说明:
    - id: id
    """

    url = "/mgmt/cms/promoCopy/delPromoCopy"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
