import os

from util.client import client

data = {
    "displayUserSerial": "",  # 关联序列号
    "relateType": 0,  # 关联类型:1.素材;2.问卷;3.直播间;4.码上有名头像框;
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_material_removeAllMaterialDisplayUser(data=data, headers=headers):
    """
    清空素材展示用户
    /mgmt/cms/material/removeAllMaterialDisplayUser

    参数说明:
    - displayUserSerial: 关联序列号
    - relateType: 关联类型:1.素材;2.问卷;3.直播间;4.码上有名头像框;
    """

    url = "/mgmt/cms/material/removeAllMaterialDisplayUser"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
