import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_rightsStatement_getContent(headers=headers):
    """
    获取权益说明内容
    /mgmt/cms/rightsStatement/getContent
    """

    url = "/mgmt/cms/rightsStatement/getContent"
    with client.get(url=url, headers=headers) as r:
        return r
