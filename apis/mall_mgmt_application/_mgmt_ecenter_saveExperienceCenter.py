import os

from util.client import client

data = {
    "address": "",  # 地址
    "centerName": "",  # 体验中心名称
    "centerProduct": "",  # 体验中心产品，示例（AG,WP1022,LAM007）
    "holidayBlacklist": "",  # 节日黑名单，日期示例（2025-05-01,2025-05-02,2025-05-03）
    "id": 0,  # 主键id
    "timeSpan": "",  # 自提时段，每周示例（周一_09:00-18:00;周二_09:00-12:00,13:30-18:00）；每天示例（09:00-12:00,13:30-18:00）
    "warehouse": "",  # 仓库
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_ecenter_saveExperienceCenter(data=data, headers=headers):
    """
    新增/编辑体验中心
    /mgmt/ecenter/saveExperienceCenter

    参数说明:
    - address: 地址
    - centerName: 体验中心名称
    - centerProduct: 体验中心产品，示例（AG,WP1022,LAM007）
    - holidayBlacklist: 节日黑名单，日期示例（2025-05-01,2025-05-02,2025-05-03）
    - id: 主键id
    - timeSpan: 自提时段，每周示例（周一_09:00-18:00;周二_09:00-12:00,13:30-18:00）；每天示例（09:00-12:00,13:30-18:00）
    - warehouse: 仓库
    """

    url = "/mgmt/ecenter/saveExperienceCenter"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
