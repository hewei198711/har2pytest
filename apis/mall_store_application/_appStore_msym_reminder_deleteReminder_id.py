import os

from util.client import client

params = {
    "id": "",  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_msym_reminder_deleteReminder_id(params=params, headers=headers):
    """
    删除店铺温馨提示语
    /appStore/msym/reminder/deleteReminder/{id}

    参数说明:
    - id: id
    """

    url = f"/appStore/msym/reminder/deleteReminder/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
