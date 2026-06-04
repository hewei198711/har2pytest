import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_traffic_query_id(params=params, headers=headers):
    """
    查询交通管制
    /mgmt/sys/traffic/query/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/sys/traffic/query/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
