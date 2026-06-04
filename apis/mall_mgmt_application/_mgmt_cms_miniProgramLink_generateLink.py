import os

from util.client import client

data = {
    "linkName": "",  # 链接名称
    "miniProgramPath": "",  # 页面路径
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_miniProgramLink_generateLink(data=data, headers=headers):
    """
    生成小程序链接
    /mgmt/cms/miniProgramLink/generateLink

    参数说明:
    - linkName: 链接名称
    - miniProgramPath: 页面路径
    """

    url = "/mgmt/cms/miniProgramLink/generateLink"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
