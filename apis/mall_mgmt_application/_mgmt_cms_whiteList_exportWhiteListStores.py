import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_whiteList_exportWhiteListStores(params=params, headers=headers):
    """
    导出白名单服务中心列表
    /mgmt/cms/whiteList/exportWhiteListStores

    参数说明:
    - storeCode: 服务中心编号
    """

    url = "/mgmt/cms/whiteList/exportWhiteListStores"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
