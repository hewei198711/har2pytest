import os

from util.client import client

params = {
    "location": 0,  # 显示位置,1:APP,2:小程序
    "shelfStatus": 0,  # 上架状态,0：待上架; 1：已上架；2：已下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_iconSetting_getIconSettingList(params=params, headers=headers):
    """
    获取Icon配置列表
    /mgmt/cms/iconSetting/getIconSettingList

    参数说明:
    - location: 显示位置,1:APP,2:小程序
    - shelfStatus: 上架状态,0：待上架; 1：已上架；2：已下架
    """

    url = "/mgmt/cms/iconSetting/getIconSettingList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
