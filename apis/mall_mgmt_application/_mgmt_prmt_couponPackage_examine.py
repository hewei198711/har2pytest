import os

from util.client import client

data = {
    "attachments": [{"fileName": "", "url": ""}],  # 附件地址集合
    "examine": 0,  # 审核是否通过:3-通过,4-不通过
    "id": 0,  # id
    "remarks": "",  # 审核意见
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponPackage_examine(data=data, headers=headers):
    """
    审核
    /mgmt/prmt/couponPackage/examine

    参数说明:
    - attachments: 附件地址集合
    - attachments.fileName: 文件名称
    - attachments.url: 文件地址
    - examine: 审核是否通过:3-通过,4-不通过
    - id: id
    - remarks: 审核意见
    """

    url = "/mgmt/prmt/couponPackage/examine"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
