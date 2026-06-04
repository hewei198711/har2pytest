import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_honor_userLevelHideListImportSave(headers=headers):
    """
    用户荣誉(会员等级隐藏)导入新增
    /mgmt/cms/honor/userLevelHideListImportSave
    """

    url = "/mgmt/cms/honor/userLevelHideListImportSave"
    with client.post(url=url, headers=headers) as r:
        return r
