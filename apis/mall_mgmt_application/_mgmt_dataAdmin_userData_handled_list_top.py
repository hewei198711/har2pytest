import os

from util.client import client

params = {
    "day": 0,  # day
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_userData_handled_list_top(params=params, headers=headers):
    """
    查询经办人(top10)
    /mgmt/dataAdmin/userData/handled/list/top

    参数说明:
    - day: day
    """

    url = "/mgmt/dataAdmin/userData/handled/list/top"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
