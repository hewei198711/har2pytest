import os

from util.client import client

params = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msym_reminder_updateReminder_id(params=params, headers=headers):
    """
    编辑修改店铺温馨提示语
    /appStore/msym/reminder/updateReminder/{id}

    参数说明:
    - id: id
    - reminderLabel: 温馨提示语内容
    """

    url = f"/appStore/msym/reminder/updateReminder/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
