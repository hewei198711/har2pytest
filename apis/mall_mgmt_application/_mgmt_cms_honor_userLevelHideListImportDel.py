import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_honor_userLevelHideListImportDel(headers=headers):
    """
    用户荣誉(会员等级隐藏)导入删除
    /mgmt/cms/honor/userLevelHideListImportDel
    """

    url = "/mgmt/cms/honor/userLevelHideListImportDel"
    with client.post(url=url, headers=headers) as r:
        return r
