import os

from util.client import client

data = {
    "content": "",  # 活动列表内容
    "detailImg": "",  # 活动详情背景图
    "isSetBg": 0,  # 是否设置背景图，0：否，1：是
    "listImg": "",  # 活动列表背景图
    "name": "",  # 活动名称
    "promotionId": 0,  # 活动ID
    "promotionType": 0,  # 活动类型(活动专区): 1.通用 2:随心购
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_activity_saveActivity(data=data, headers=headers):
    """
    新增活动
    /mgmt/cms/activity/saveActivity

    参数说明:
    - content: 活动列表内容
    - detailImg: 活动详情背景图
    - isSetBg: 是否设置背景图，0：否，1：是
    - listImg: 活动列表背景图
    - name: 活动名称
    - promotionId: 活动ID
    - promotionType: 活动类型(活动专区): 1.通用 2:随心购
    - sort: 排序
    """

    url = "/mgmt/cms/activity/saveActivity"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
