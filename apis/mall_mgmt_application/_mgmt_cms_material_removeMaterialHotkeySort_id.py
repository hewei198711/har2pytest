import os

from util.client import client

params = {
    "id": "",  # 热词id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_removeMaterialHotkeySort_id(params=params, headers=headers):
    """
    素材管理-删除热词
    /mgmt/cms/material/removeMaterialHotkeySort/{id}

    参数说明:
    - id: 热词id
    """

    url = f"/mgmt/cms/material/removeMaterialHotkeySort/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
