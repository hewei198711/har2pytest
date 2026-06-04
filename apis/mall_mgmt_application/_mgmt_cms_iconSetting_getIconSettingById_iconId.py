import os

from util.client import client

params = {
    "iconId": 0,  # iconId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_iconSetting_getIconSettingById_iconId(params=params, headers=headers):
    """
    根据ID查询icon配置
    /mgmt/cms/iconSetting/getIconSettingById/{iconId}

    参数说明:
    - iconId: iconId
    """

    url = f"/mgmt/cms/iconSetting/getIconSettingById/{params['iconId']}"
    with client.get(url=url, headers=headers) as r:
        return r
