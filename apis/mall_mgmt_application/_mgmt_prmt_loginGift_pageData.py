import os

from util.client import client

params = {
    "endTime": "",  # 数据时间止区(yyyy-MM-dd)
    "id": 0,  # 登录提醒id
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "platform": 0,  # 数据平台:1-APP,2-PC,4-小程序
    "startTime": "",  # 数据时间起区(yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_pageData(params=params, headers=headers):
    """
    分页查询活动数据
    /mgmt/prmt/loginGift/pageData

    参数说明:
    - endTime: 数据时间止区(yyyy-MM-dd)
    - id: 登录提醒id
    - pageNum: 当前页
    - pageSize: 每页数量
    - platform: 数据平台:1-APP,2-PC,4-小程序
    - startTime: 数据时间起区(yyyy-MM-dd)
    """

    url = "/mgmt/prmt/loginGift/pageData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
