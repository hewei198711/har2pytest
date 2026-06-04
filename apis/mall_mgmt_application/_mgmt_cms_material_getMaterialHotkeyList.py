import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_getMaterialHotkeyList(headers=headers):
    """
    素材管理-查询搜索热词列表
    /mgmt/cms/material/getMaterialHotkeyList
    """

    url = "/mgmt/cms/material/getMaterialHotkeyList"
    with client.get(url=url, headers=headers) as r:
        return r
