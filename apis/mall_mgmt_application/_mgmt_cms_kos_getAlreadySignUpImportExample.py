import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_getAlreadySignUpImportExample(headers=headers):
    """
    已报名人员名单导入模板
    /mgmt/cms/kos/getAlreadySignUpImportExample
    """

    url = "/mgmt/cms/kos/getAlreadySignUpImportExample"
    with client.get(url=url, headers=headers) as r:
        return r
