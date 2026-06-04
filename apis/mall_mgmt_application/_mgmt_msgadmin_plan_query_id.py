import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_plan_query_id(params=params, headers=headers):
    """
    查询单个发送计划（系统消息）接口
    /mgmt/msgadmin/plan/query/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/msgadmin/plan/query/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
