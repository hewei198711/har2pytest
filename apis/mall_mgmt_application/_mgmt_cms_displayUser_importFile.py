import os
from urllib.parse import urlencode

from util.client import client

data = {
    "displayUserSerial": "",  # 展示用户关联序列号
    "relateType": "",  # 关联类型:1.素材;2.问卷;3.直播间;4.码上有名头像框;
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_displayUser_importFile(data=data, headers=headers):
    """
    展示用户导入
    /mgmt/cms/displayUser/importFile

    参数说明:
    - displayUserSerial: 展示用户关联序列号
    - relateType: 关联类型:1.素材;2.问卷;3.直播间;4.码上有名头像框;
    """

    url = "/mgmt/cms/displayUser/importFile"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
