import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_typeLabel_queryTypeLabelById_id(params=params, headers=headers):
    """
    查询类型标签
    /mgmt/cms/typeLabel/queryTypeLabelById/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/cms/typeLabel/queryTypeLabelById/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
