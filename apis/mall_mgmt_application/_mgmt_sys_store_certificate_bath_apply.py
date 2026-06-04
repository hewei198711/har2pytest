import os

from util.client import client

data = {
    "bathApplyList": [{"applyReason": "", "downloadDeadline": "", "storeCode": ""}],  # 服务中心申请集合
    "certificateList": [],  # 证件列表id集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_store_certificate_bath_apply(data=data, headers=headers):
    """
    批量发起公司证件申请
    /mgmt/sys/store/certificate/bath/apply

    参数说明:
    - bathApplyList: 服务中心申请集合
    - certificateList: 证件列表id集合
    """

    url = "/mgmt/sys/store/certificate/bath/apply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
