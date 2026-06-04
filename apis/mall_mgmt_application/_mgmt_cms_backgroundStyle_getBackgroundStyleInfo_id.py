import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_backgroundStyle_getBackgroundStyleInfo_id(params=params, headers=headers):
    """
    获取背景样式信息
    /mgmt/cms/backgroundStyle/getBackgroundStyleInfo/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/cms/backgroundStyle/getBackgroundStyleInfo/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
