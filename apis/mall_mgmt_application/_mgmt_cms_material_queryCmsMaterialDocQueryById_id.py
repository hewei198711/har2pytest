import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_queryCmsMaterialDocQueryById_id(params=params, headers=headers):
    """
    查询素材-文档
    /mgmt/cms/material/queryCmsMaterialDocQueryById/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/cms/material/queryCmsMaterialDocQueryById/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
