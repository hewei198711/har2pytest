import os

from util.client import client

data = {
    "shelfStatus": 0,  # 下架状态
    "themeId": 0,  # 主题id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_category_shelfOff(data=data, headers=headers):
    """
    主题下架
    /mgmt/cms/category/shelfOff

    参数说明:
    - shelfStatus: 下架状态
    - themeId: 主题id
    """

    url = "/mgmt/cms/category/shelfOff"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
