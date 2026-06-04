import os

from util.client import client

data = {
    "enclosureVos": [{"fileName": "", "urls": ""}],  # 附件集合
    "examine": 0,  # 审核是否通过3通过4不通过
    "remarks": "",  # 备注
    "shareTaskId": 0,  # 分享活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_examine(data=data, headers=headers):
    """
    审核
    /mgmt/prmt/share/examine

    参数说明:
    - enclosureVos: 附件集合
    - enclosureVos.fileName: 附件名称
    - enclosureVos.urls: 附件地址
    - examine: 审核是否通过3通过4不通过
    - remarks: 备注
    - shareTaskId: 分享活动id
    """

    url = "/mgmt/prmt/share/examine"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
