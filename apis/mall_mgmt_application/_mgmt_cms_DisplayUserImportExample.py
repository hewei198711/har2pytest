import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_DisplayUserImportExample(headers=headers):
    """
    展示用户导入模板
    /mgmt/cms/DisplayUserImportExample
    """

    url = "/mgmt/cms/DisplayUserImportExample"
    with client.get(url=url, headers=headers) as r:
        return r
