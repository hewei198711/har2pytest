import os

from util.client import client

data = {
    "link": "",  # 链接
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_specialLink_getPickUpFeeLink(data=data, headers=headers):
    """
    保存上门取件收费说明链接地址
    /mgmt/cms/specialLink/getPickUpFeeLink

    参数说明:
    - link: 链接
    """

    url = "/mgmt/cms/specialLink/getPickUpFeeLink"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
