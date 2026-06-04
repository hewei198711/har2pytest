import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_getKosSetting(headers=headers):
    """
    获取kos报名配置
    /mgmt/cms/kos/getKosSetting
    """

    url = "/mgmt/cms/kos/getKosSetting"
    with client.get(url=url, headers=headers) as r:
        return r
