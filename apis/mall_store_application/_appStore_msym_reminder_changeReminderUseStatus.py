import os

from util.client import client

data = {
    "enable": 0,  # 是否启用, 0:禁用; 1:启用
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msym_reminder_changeReminderUseStatus(data=data, headers=headers):
    """
    修改店铺温馨提示语使用状态
    /appStore/msym/reminder/changeReminderUseStatus

    参数说明:
    - enable: 是否启用, 0:禁用; 1:启用
    - id: id
    """

    url = "/appStore/msym/reminder/changeReminderUseStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
