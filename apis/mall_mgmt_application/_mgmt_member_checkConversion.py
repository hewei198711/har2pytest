import os

from util.client import client

params = {
    "id": "",  # 顾客ID
    "toMemberType": "",  # 目标身份标识：2->优惠顾客; 3->云商; 4->微店。
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_checkConversion(params=params, headers=headers):
    """
    身份转换检查接口
    /mgmt/member/checkConversion

    参数说明:
    - id: 顾客ID
    - toMemberType: 目标身份标识：2->优惠顾客; 3->云商; 4->微店。
    """

    url = "/mgmt/member/checkConversion"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
