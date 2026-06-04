import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_addAllowSignUpList(data=data, headers=headers):
    """
    可报名人员单个新增
    /mgmt/cms/kos/addAllowSignUpList

    参数说明:
    - cardNo: 会员卡号
    """

    url = "/mgmt/cms/kos/addAllowSignUpList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
