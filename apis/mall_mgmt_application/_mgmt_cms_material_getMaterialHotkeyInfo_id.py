import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_getMaterialHotkeyInfo_id(params=params, headers=headers):
    """
    素材管理-热词详情查询
    /mgmt/cms/material/getMaterialHotkeyInfo/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/cms/material/getMaterialHotkeyInfo/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
