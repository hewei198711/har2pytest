import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_backgroundStyle_editBackgroundStyle_id(params=params, headers=headers):
    """
    修改背景样式信息
    /mgmt/cms/backgroundStyle/editBackgroundStyle/{id}

    参数说明:
    - id: id
    - enableStatus: 启用状态: 0.禁用 1.启用
    - isDefault: 是否默认: 0.否 1.是
    - memberTypes: 展示对象 1:会员; 2:vip会员; 3:云商; 4:微店;(多选使用逗号分隔)
    - sort: 排序
    - url: 链接
    """

    url = f"/mgmt/cms/backgroundStyle/editBackgroundStyle/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
