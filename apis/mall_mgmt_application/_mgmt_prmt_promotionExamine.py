import os

from util.client import client

data = {
    "enclosureVos": [{"fileName": "", "urls": ""}],  # 附件集合
    "examine": 0,  # 审核是否通过3通过4不通过
    "promotionId": 0,  # 活动id
    "remarks": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_promotionExamine(data=data, headers=headers):
    """
    活动审核
    /mgmt/prmt/promotionExamine

    参数说明:
    - enclosureVos: 附件集合
    - enclosureVos.fileName: 附件名称
    - enclosureVos.urls: 附件地址
    - examine: 审核是否通过3通过4不通过
    - promotionId: 活动id
    - remarks: 备注
    """

    url = "/mgmt/prmt/promotionExamine"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
