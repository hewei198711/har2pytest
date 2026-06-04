import os

from util.client import client

data = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_magicHomePage_querySwitchRecordList(data=data, headers=headers):
    """
    获取历史开关记录列表
    /mgmt/cms/magicHomePage/querySwitchRecordList

    参数说明:
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/cms/magicHomePage/querySwitchRecordList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
