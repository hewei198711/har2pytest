import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_honor_userHonorImportSave(headers=headers):
    """
    用户荣誉导入新增
    /mgmt/cms/honor/userHonorImportSave
    """

    url = "/mgmt/cms/honor/userHonorImportSave"
    with client.post(url=url, headers=headers) as r:
        return r
