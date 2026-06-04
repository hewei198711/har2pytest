import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_logo_getLogoConfig(headers=headers):
    """
    获取logo配置
    /mgmt/cms/logo/getLogoConfig
    """

    url = "/mgmt/cms/logo/getLogoConfig"
    with client.get(url=url, headers=headers) as r:
        return r
