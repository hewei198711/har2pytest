import os

from util.client import client

data = {
    "content": "",  # 说明内容
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_avatar_saveStatement(data=data, headers=headers):
    """
    保存头像说明内容
    /mgmt/cms/avatar/saveStatement

    参数说明:
    - content: 说明内容
    """

    url = "/mgmt/cms/avatar/saveStatement"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
