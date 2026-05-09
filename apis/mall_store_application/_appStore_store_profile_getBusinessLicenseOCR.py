import os
from urllib.parse import urlencode

from util.client import client

data = {
    "fullFilePath": "",  # 图片全路径
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_store_profile_getBusinessLicenseOCR(data=data, headers=headers):
    """
    获取营业执照识别结果
    /appStore/store/profile/getBusinessLicenseOCR

    参数说明:
    - fullFilePath: 图片全路径
    """

    url = "/appStore/store/profile/getBusinessLicenseOCR"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
