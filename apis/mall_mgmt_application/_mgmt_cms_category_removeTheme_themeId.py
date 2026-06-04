import os

from util.client import client

params = {
    "themeId": 0,  # themeId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_category_removeTheme_themeId(params=params, headers=headers):
    """
    删除主题
    /mgmt/cms/category/removeTheme/{themeId}

    参数说明:
    - themeId: themeId
    """

    url = f"/mgmt/cms/category/removeTheme/{params['themeId']}"
    with client.get(url=url, headers=headers) as r:
        return r
