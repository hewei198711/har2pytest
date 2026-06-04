import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_materialDisplayUserImportExample(headers=headers):
    """
    素材展示用户导入模板
    /mgmt/cms/material/materialDisplayUserImportExample
    """

    url = "/mgmt/cms/material/materialDisplayUserImportExample"
    with client.get(url=url, headers=headers) as r:
        return r
