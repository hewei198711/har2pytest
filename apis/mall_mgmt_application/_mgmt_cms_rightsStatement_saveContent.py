import os

from util.client import client

data = {
    "content": "",  # 说明内容
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_rightsStatement_saveContent(data=data, headers=headers):
    """
    保存权益说明内容
    /mgmt/cms/rightsStatement/saveContent

    参数说明:
    - content: 说明内容
    """

    url = "/mgmt/cms/rightsStatement/saveContent"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
