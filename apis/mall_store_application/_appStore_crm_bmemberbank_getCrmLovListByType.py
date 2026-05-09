import os

from util.client import client

params = {
    "dictType": "",  # dictType
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_crm_bmemberbank_getCrmLovListByType(params=params, headers=headers):
    """
    根据业务类型获取字典列表
    /appStore/crm/bmemberbank/getCrmLovListByType

    参数说明:
    - dictType: dictType
    """

    url = "/appStore/crm/bmemberbank/getCrmLovListByType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
