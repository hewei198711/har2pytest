import os

from util.client import client

params = {
    "certificatesNo": "",  # 配偶证件号
    "certificatesType": "",  # 配偶证件类型：1->身份证；2->其他
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_member_checkOpenableBySpouseCertificatesNo(params=params, headers=headers):
    """
    根据配偶证件号码查询是否能开卡
    /mgmt/member/checkOpenableBySpouseCertificatesNo

    参数说明:
    - certificatesNo: 配偶证件号
    - certificatesType: 配偶证件类型：1->身份证；2->其他
    """

    url = "/mgmt/member/checkOpenableBySpouseCertificatesNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
