import os
from urllib.parse import urlencode

from util.client import client

data = {
    "type": 0,  # type
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_msgadmin_handmade_uploadFile(data=data, headers=headers):
    """
    上传附件/导入名单
    /mgmt/msgadmin/handmade/uploadFile

    参数说明:
    - type: type
    """

    url = "/mgmt/msgadmin/handmade/uploadFile"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
