import os

from util.client import client

params = {
    "day": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_userData_handled_list_detail(params=params, headers=headers):
    """
    查询经办人明细
    /mgmt/dataAdmin/userData/handled/list/detail
    """

    url = "/mgmt/dataAdmin/userData/handled/list/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
