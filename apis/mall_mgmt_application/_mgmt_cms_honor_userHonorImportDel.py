import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_honor_userHonorImportDel(headers=headers):
    """
    用户荣誉导入删除
    /mgmt/cms/honor/userHonorImportDel
    """

    url = "/mgmt/cms/honor/userHonorImportDel"
    with client.post(url=url, headers=headers) as r:
        return r
