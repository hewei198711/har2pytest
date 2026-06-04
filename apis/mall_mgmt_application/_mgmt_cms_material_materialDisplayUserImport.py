import os
from urllib.parse import urlencode

from util.client import client

data = {
    "displayUserSerial": "",  # 素材展示用户关联序列号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_cms_material_materialDisplayUserImport(data=data, headers=headers):
    """
    素材展示用户导入
    /mgmt/cms/material/materialDisplayUserImport

    参数说明:
    - displayUserSerial: 素材展示用户关联序列号
    """

    url = "/mgmt/cms/material/materialDisplayUserImport"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
