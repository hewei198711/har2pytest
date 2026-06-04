import os

from util.client import client

data = {
    "id": 0,  # id(编辑时传入)
    "medalIcon": "",  # 勋章图标
    "medalLevel": 0,  # 勋章等级
    "medalTitle": "",  # 勋章名称
    "requiredGuardianPower": 0,  # 需要满足的守护能量条件
    "rightsIdList": [],  # 权益id列表
    "shelfConfig": 0,  # 上下架配置,1:立即上架; 2:定时上架;
    "shelfUpTime": "",  # 上架时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_charity_medal_edit(data=data, headers=headers):
    """
    编辑公益购勋章信息
    /mgmt/cms/charity/medal/edit

    参数说明:
    - id: id(编辑时传入)
    - medalIcon: 勋章图标
    - medalLevel: 勋章等级
    - medalTitle: 勋章名称
    - requiredGuardianPower: 需要满足的守护能量条件
    - rightsIdList: 权益id列表
    - shelfConfig: 上下架配置,1:立即上架; 2:定时上架;
    - shelfUpTime: 上架时间
    """

    url = "/mgmt/cms/charity/medal/edit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
