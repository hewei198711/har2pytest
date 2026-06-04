import os

from util.client import client

params = {
    "toolId": 0,  # toolId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getToolDetailById_toolId(params=params, headers=headers):
    """
    根据id获取工具详情数据
    /mgmt/cms/getToolDetailById/{toolId}

    参数说明:
    - toolId: toolId
    """

    url = f"/mgmt/cms/getToolDetailById/{params['toolId']}"
    with client.get(url=url, headers=headers) as r:
        return r
