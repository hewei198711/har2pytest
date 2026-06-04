import os

from util.client import client

data = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_whiteList_queryWhiteListStoreList(data=data, headers=headers):
    """
    获取白名单服务中心列表
    /mgmt/cms/whiteList/queryWhiteListStoreList

    参数说明:
    - pageNum: 页码
    - pageSize: 每页页数
    - storeCode: 服务中心编号
    """

    url = "/mgmt/cms/whiteList/queryWhiteListStoreList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
