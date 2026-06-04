import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_cleaner_log_list_id(params=params, headers=headers):
    """
    获取清洗人员协议日志列表
    /mgmt/acc/cleaner/log/list/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/acc/cleaner/log/list/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
