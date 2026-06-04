import os

from util.client import client

data = {
    "location": 0,  # 显示位置 （1:PC，2：APP，3：小程序）
    "shelfStatus": 0,  # 上架状态,0：待上架; 1：已上架；2：已下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_category_getThemeList(data=data, headers=headers):
    """
    获取主题列表
    /mgmt/cms/category/getThemeList

    参数说明:
    - location: 显示位置 （1:PC，2：APP，3：小程序）
    - shelfStatus: 上架状态,0：待上架; 1：已上架；2：已下架
    """

    url = "/mgmt/cms/category/getThemeList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
