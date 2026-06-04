import os

from util.client import client

params = {
    "activityId": 0,  # activityId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_activity_editActivity_activityId(params=params, headers=headers):
    """
    编辑活动
    /mgmt/cms/activity/editActivity/{activityId}

    参数说明:
    - activityId: activityId
    - content: 活动列表内容
    - detailImg: 活动详情背景图
    - isSetBg: 是否设置背景图，0：否，1：是
    - listImg: 活动列表背景图
    - name: 活动名称
    - promotionId: 活动ID
    - promotionType: 活动类型(活动专区): 1.通用 2:随心购
    - sort: 排序
    """

    url = f"/mgmt/cms/activity/editActivity/{params['activityId']}"
    with client.get(url=url, headers=headers) as r:
        return r
