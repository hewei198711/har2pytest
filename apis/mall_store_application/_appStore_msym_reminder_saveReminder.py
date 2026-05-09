import os

from util.client import client

data = {
    "reminderLabel": "",  # 温馨提示语内容
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msym_reminder_saveReminder(data=data, headers=headers):
    """
    新增店铺温馨提示语
    /appStore/msym/reminder/saveReminder

    参数说明:
    - reminderLabel: 温馨提示语内容
    """

    url = "/appStore/msym/reminder/saveReminder"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
