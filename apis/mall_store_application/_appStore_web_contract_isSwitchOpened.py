import os

from util.client import client

params = {
    "switchType": "",  # 开关类型：1、钱包对账单开关
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_contract_isSwitchOpened(params=params, headers=headers):
    """
    通过类型查询打印开关是否开启
    /appStore/web/contract/isSwitchOpened

    参数说明:
    - switchType: 开关类型：1、钱包对账单开关
    """

    url = "/appStore/web/contract/isSwitchOpened"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
