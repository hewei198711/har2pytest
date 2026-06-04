import os

from util.client import client

data = {
    "applyReason": "",  # 申请原因
    "applyVoucher": [],  # 申请凭证
    "certificateList": [],  # 证件列表id集合
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_store_certificate_apply(data=data, headers=headers):
    """
    发起公司证件申请
    /mgmt/sys/store/certificate/apply

    参数说明:
    - applyReason: 申请原因
    - applyVoucher: 申请凭证
    - certificateList: 证件列表id集合
    - storeCode: 服务中心编码
    """

    url = "/mgmt/sys/store/certificate/apply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
