import os

from util.client import client

params = {
    "certificatesNo": "",  # 证件号
    "certificatesType": "",  # 证件类型：1->身份证；2->其他
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_checkOpenableByCertificatesNo(params=params, headers=headers):
    """
    根据证件号码查询是否能开卡
    /mgmt/member/checkOpenableByCertificatesNo

    参数说明:
    - certificatesNo: 证件号
    - certificatesType: 证件类型：1->身份证；2->其他
    """

    url = "/mgmt/member/checkOpenableByCertificatesNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
