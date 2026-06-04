import os
from urllib.parse import urlencode

from util.client import client

data = {
    "modelName": "",  # modelName
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_annualReview_getConfigByModelName(data=data, headers=headers):
    """
    根据年审模块配置名称获取年审模块配置信息
    /mgmt/store/annualReview/getConfigByModelName

    参数说明:
    - modelName: modelName
    """

    url = "/mgmt/store/annualReview/getConfigByModelName"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
