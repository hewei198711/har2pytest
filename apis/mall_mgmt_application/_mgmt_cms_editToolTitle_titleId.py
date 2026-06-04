import os

from util.client import client

params = {
    "titleId": 0,  # titleId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_editToolTitle_titleId(params=params, headers=headers):
    """
    编辑工具PC类型标题
    /mgmt/cms/editToolTitle/{titleId}

    参数说明:
    - sort: 排序
    - title: PC类型标题
    - titleId: titleId
    """

    url = f"/mgmt/cms/editToolTitle/{params['titleId']}"
    with client.get(url=url, headers=headers) as r:
        return r
