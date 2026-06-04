import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_honor_UserHonorImportExample(headers=headers):
    """
    用户荣誉导入模板
    /mgmt/cms/honor/UserHonorImportExample
    """

    url = "/mgmt/cms/honor/UserHonorImportExample"
    with client.get(url=url, headers=headers) as r:
        return r
