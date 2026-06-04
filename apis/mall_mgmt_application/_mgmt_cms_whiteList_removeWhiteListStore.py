import os

from util.client import client

data = {
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_whiteList_removeWhiteListStore(data=data, headers=headers):
    """
    删除指定白名单服务中心
    /mgmt/cms/whiteList/removeWhiteListStore

    参数说明:
    - storeCode: 服务中心编号
    """

    url = "/mgmt/cms/whiteList/removeWhiteListStore"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
