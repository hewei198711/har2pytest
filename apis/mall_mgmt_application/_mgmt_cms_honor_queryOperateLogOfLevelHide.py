import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "endTime": "",  # 结束时间(操作时间yyyy-MM-dd)
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "startTime": "",  # 开始时间(操作时间yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_honor_queryOperateLogOfLevelHide(data=data, headers=headers):
    """
    查询用户荣誉(会员等级隐藏)相关的操作记录
    /mgmt/cms/honor/queryOperateLogOfLevelHide

    参数说明:
    - cardNo: 会员卡号
    - endTime: 结束时间(操作时间yyyy-MM-dd)
    - pageNum: 页码
    - pageSize: 每页页数
    - startTime: 开始时间(操作时间yyyy-MM-dd)
    """

    url = "/mgmt/cms/honor/queryOperateLogOfLevelHide"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
