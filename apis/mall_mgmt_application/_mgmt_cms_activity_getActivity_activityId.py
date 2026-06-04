import os

from util.client import client

params = {
    "activityId": 0,  # activityId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_activity_getActivity_activityId(params=params, headers=headers):
    """
    根据id查询活动
    /mgmt/cms/activity/getActivity/{activityId}

    参数说明:
    - activityId: activityId
    """

    url = f"/mgmt/cms/activity/getActivity/{params['activityId']}"
    with client.get(url=url, headers=headers) as r:
        return r
