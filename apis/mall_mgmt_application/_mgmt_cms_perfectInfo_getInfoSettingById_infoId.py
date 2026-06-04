import os

from util.client import client

params = {
    "infoId": 0,  # infoId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_perfectInfo_getInfoSettingById_infoId(params=params, headers=headers):
    """
    获取完美资讯信息
    /mgmt/cms/perfectInfo/getInfoSettingById/{infoId}

    参数说明:
    - infoId: infoId
    """

    url = f"/mgmt/cms/perfectInfo/getInfoSettingById/{params['infoId']}"
    with client.get(url=url, headers=headers) as r:
        return r
