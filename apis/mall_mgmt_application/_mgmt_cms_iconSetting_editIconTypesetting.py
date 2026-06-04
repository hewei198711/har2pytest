import os

from util.client import client

data = {
    "displayStyle": 0,  # 展示样式选择: 1.横向滑动 2.自动换行
    "location": 0,  # 显示位置,1:APP,2:小程序
    "typesetting": 0,  # 每页排版数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_iconSetting_editIconTypesetting(data=data, headers=headers):
    """
    保存icon排版
    /mgmt/cms/iconSetting/editIconTypesetting

    参数说明:
    - displayStyle: 展示样式选择: 1.横向滑动 2.自动换行
    - location: 显示位置,1:APP,2:小程序
    - typesetting: 每页排版数量
    """

    url = "/mgmt/cms/iconSetting/editIconTypesetting"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
