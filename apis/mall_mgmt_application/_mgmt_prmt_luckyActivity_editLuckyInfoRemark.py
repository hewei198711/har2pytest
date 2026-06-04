import os

from util.client import client

data = {
    "activityId": 0,  # 活动id
    "modifyModule": 0,  # 修改模块类型(16-分享助力小程序分享卡片文案)
    "remark": "",  # 文案
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_editLuckyInfoRemark(data=data, headers=headers):
    """
    修改抽奖活动详情页面的相关文案 16-分享助力小程序分享卡片文案
    /mgmt/prmt/luckyActivity/editLuckyInfoRemark

    参数说明:
    - activityId: 活动id
    - modifyModule: 修改模块类型(16-分享助力小程序分享卡片文案)
    - remark: 文案
    """

    url = "/mgmt/prmt/luckyActivity/editLuckyInfoRemark"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
