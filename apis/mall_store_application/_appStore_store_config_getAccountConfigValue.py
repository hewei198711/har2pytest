import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_config_getAccountConfigValue(headers=headers):
    """
    服务费展示开关配置，配置值，1：开启，0：关闭
    /appStore/store/config/getAccountConfigValue
    """

    url = "/appStore/store/config/getAccountConfigValue"
    with client.get(url=url, headers=headers) as r:
        return r
