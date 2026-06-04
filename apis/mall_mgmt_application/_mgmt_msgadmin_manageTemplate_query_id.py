import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_manageTemplate_query_id(params=params, headers=headers):
    """
    获取一个站内信模板内容
    /mgmt/msgadmin/manageTemplate/query/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/msgadmin/manageTemplate/query/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
