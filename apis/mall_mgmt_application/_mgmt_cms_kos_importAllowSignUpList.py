import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_kos_importAllowSignUpList(headers=headers):
    """
    可报名人员名单导入
    /mgmt/cms/kos/importAllowSignUpList
    """

    url = "/mgmt/cms/kos/importAllowSignUpList"
    with client.post(url=url, headers=headers) as r:
        return r
