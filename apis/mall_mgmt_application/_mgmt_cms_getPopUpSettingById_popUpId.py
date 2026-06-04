import os

from util.client import client

params = {
    "popUpId": 0,  # popUpId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getPopUpSettingById_popUpId(params=params, headers=headers):
    """
    根据id获取弹窗配置
    /mgmt/cms/getPopUpSettingById/{popUpId}

    参数说明:
    - popUpId: popUpId
    """

    url = f"/mgmt/cms/getPopUpSettingById/{params['popUpId']}"
    with client.get(url=url, headers=headers) as r:
        return r
