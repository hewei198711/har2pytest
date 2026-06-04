import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatar_getStatement(headers=headers):
    """
    获取头像说明内容
    /mgmt/cms/avatar/getStatement
    """

    url = "/mgmt/cms/avatar/getStatement"
    with client.get(url=url, headers=headers) as r:
        return r
