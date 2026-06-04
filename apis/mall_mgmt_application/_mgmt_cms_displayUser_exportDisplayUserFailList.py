import os

from util.client import client

params = {
    "displayUserSerial": "",  # 展示用户关联序列号
    "relateType": 0,  # relateType
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_displayUser_exportDisplayUserFailList(params=params, headers=headers):
    """
    导出展示用户导入失败原因列表
    /mgmt/cms/displayUser/exportDisplayUserFailList

    参数说明:
    - displayUserSerial: 展示用户关联序列号
    - relateType: relateType
    """

    url = "/mgmt/cms/displayUser/exportDisplayUserFailList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
