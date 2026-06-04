import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_getAllowSignUpImportExample(headers=headers):
    """
    可报名人员名单导入模板
    /mgmt/cms/kos/getAllowSignUpImportExample
    """

    url = "/mgmt/cms/kos/getAllowSignUpImportExample"
    with client.get(url=url, headers=headers) as r:
        return r
