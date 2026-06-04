import os

from util.client import client

data = {
    "content": "",  # 说明内容
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatarFrame_saveStatement(data=data, headers=headers):
    """
    保存头像框说明内容
    /mgmt/cms/avatarFrame/saveStatement

    参数说明:
    - content: 说明内容
    """

    url = "/mgmt/cms/avatarFrame/saveStatement"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
