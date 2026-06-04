import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_kos_importAlreadySignUpList(headers=headers):
    """
    已报名人员名单导入
    /mgmt/cms/kos/importAlreadySignUpList
    """

    url = "/mgmt/cms/kos/importAlreadySignUpList"
    with client.post(url=url, headers=headers) as r:
        return r
