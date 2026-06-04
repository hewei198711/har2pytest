import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_iconSetting_getIconTypesetting(headers=headers):
    """
    获取icon排版信息
    /mgmt/cms/iconSetting/getIconTypesetting
    """

    url = "/mgmt/cms/iconSetting/getIconTypesetting"
    with client.get(url=url, headers=headers) as r:
        return r
