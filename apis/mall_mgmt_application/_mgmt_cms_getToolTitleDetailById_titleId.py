import os

from util.client import client

params = {
    "titleId": 0,  # titleId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getToolTitleDetailById_titleId(params=params, headers=headers):
    """
    根据id获取工具PC类型标题详情数据
    /mgmt/cms/getToolTitleDetailById/{titleId}

    参数说明:
    - titleId: titleId
    """

    url = f"/mgmt/cms/getToolTitleDetailById/{params['titleId']}"
    with client.get(url=url, headers=headers) as r:
        return r
