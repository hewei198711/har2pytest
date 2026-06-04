import os

from util.client import client

data = {
    "id": 0,  # id(编辑时传入)
    "rightsIcon": "",  # 权益图标
    "rightsTitle": "",  # 权益名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_charity_guardianRights_save(data=data, headers=headers):
    """
    保存公益购守护者权益信息
    /mgmt/cms/charity/guardianRights/save

    参数说明:
    - id: id(编辑时传入)
    - rightsIcon: 权益图标
    - rightsTitle: 权益名称
    """

    url = "/mgmt/cms/charity/guardianRights/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
