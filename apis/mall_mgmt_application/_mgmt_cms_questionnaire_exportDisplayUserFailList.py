import os

from util.client import client

params = {
    "displayUserSerial": "",  # 展示用户关联序列号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_questionnaire_exportDisplayUserFailList(params=params, headers=headers):
    """
    导出问卷展示用户导入失败原因列表
    /mgmt/cms/questionnaire/exportDisplayUserFailList

    参数说明:
    - displayUserSerial: 展示用户关联序列号
    """

    url = "/mgmt/cms/questionnaire/exportDisplayUserFailList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
