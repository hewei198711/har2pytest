import os

from util.client import client

params = {
    "type": "",  # 模板类型：1.荣誉称号批量删除模板; 2.荣誉徽章批量导入模板; 3.荣誉徽章批量删除模板;
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_honor_UserHonorCardNoImportExample(params=params, headers=headers):
    """
    用户荣誉(卡号)导入模板
    /mgmt/cms/honor/UserHonorCardNoImportExample

    参数说明:
    - type: 模板类型：1.荣誉称号批量删除模板; 2.荣誉徽章批量导入模板; 3.荣誉徽章批量删除模板;
    """

    url = "/mgmt/cms/honor/UserHonorCardNoImportExample"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
