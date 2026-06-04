import os

from util.client import client

data = {
    "enable": 0,  # 是否启用, 0:禁用; 1:启用
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_promoCopy_changePromoCopyStatus(data=data, headers=headers):
    """
    促单词条状态变更接口
    /mgmt/cms/promoCopy/changePromoCopyStatus

    参数说明:
    - enable: 是否启用, 0:禁用; 1:启用
    - id: id
    """

    url = "/mgmt/cms/promoCopy/changePromoCopyStatus"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
