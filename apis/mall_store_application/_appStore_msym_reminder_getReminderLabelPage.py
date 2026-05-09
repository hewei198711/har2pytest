import os

from util.client import client

data = {
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "queryContent": "",  # 查询内容
    "reminderStatus": 0,  # 状态 0:待审核; 1:审核通过 2:审核不通过 3:管理员禁用 不传/其他值:全部
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msym_reminder_getReminderLabelPage(data=data, headers=headers):
    """
    获取店铺温馨提示语分页
    /appStore/msym/reminder/getReminderLabelPage

    参数说明:
    - pageNum: 页码
    - pageSize: 每页页数
    - queryContent: 查询内容
    - reminderStatus: 状态 0:待审核; 1:审核通过 2:审核不通过 3:管理员禁用 不传/其他值:全部
    """

    url = "/appStore/msym/reminder/getReminderLabelPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
