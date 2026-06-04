import os

from util.client import client

params = {
    "location": 0,  # 显示位置 2：APP，3：小程序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_personalTool_getToolCategoryList_location(params=params, headers=headers):
    """
    获取icon分类列表(已启用)
    /mgmt/cms/personalTool/getToolCategoryList/{location}

    参数说明:
    - location: 显示位置 2：APP，3：小程序
    """

    url = f"/mgmt/cms/personalTool/getToolCategoryList/{params['location']}"
    with client.get(url=url, headers=headers) as r:
        return r
