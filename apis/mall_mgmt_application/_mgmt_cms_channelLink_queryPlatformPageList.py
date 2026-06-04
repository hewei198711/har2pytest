import os

from util.client import client

params = {
    "platform": "",  # 平台: 1.油葱商城 2.油葱健康 3.油葱学堂 4.荟有趣
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_channelLink_queryPlatformPageList(params=params, headers=headers):
    """
    根据平台查询页面下拉列表
    /mgmt/cms/channelLink/queryPlatformPageList

    参数说明:
    - platform: 平台: 1.油葱商城 2.油葱健康 3.油葱学堂 4.荟有趣
    """

    url = "/mgmt/cms/channelLink/queryPlatformPageList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
