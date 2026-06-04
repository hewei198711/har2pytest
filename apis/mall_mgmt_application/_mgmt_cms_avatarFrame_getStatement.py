import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatarFrame_getStatement(headers=headers):
    """
    获取头像框说明内容
    /mgmt/cms/avatarFrame/getStatement
    """

    url = "/mgmt/cms/avatarFrame/getStatement"
    with client.get(url=url, headers=headers) as r:
        return r
