import os

from util.client import client

data = {
    "copyId": 0,  # 促单词条id(新增不传)
    "serialNoList": [],  # 商品编码列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_promoCopy_checkPromoCopyProductExist(data=data, headers=headers):
    """
    促单词条商品校验接口
    /mgmt/cms/promoCopy/checkPromoCopyProductExist

    参数说明:
    - copyId: 促单词条id(新增不传)
    - serialNoList: 商品编码列表
    """

    url = "/mgmt/cms/promoCopy/checkPromoCopyProductExist"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
