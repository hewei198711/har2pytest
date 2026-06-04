import os

from util.client import client

data = {
    "applyScene": [],  # 适用场景 1.公众号 2.线下海报 3.线上活动
    "channelName": "",  # 渠道名称
    "createTimeQueryEnd": "",  # 添加日期查询结束时间
    "createTimeQueryStart": "",  # 添加日期查询开始时间
    "export": False,  # TODO: 添加参数说明
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
    "platform": [],  # 平台: 1.油葱商城 2.油葱健康 3.油葱学堂 4.荟友趣
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_channelLink_exportChannelLinkPage(data=data, headers=headers):
    """
    渠道链接列表导出
    /mgmt/cms/channelLink/exportChannelLinkPage

    参数说明:
    - applyScene: 适用场景 1.公众号 2.线下海报 3.线上活动
    - channelName: 渠道名称
    - createTimeQueryEnd: 添加日期查询结束时间
    - createTimeQueryStart: 添加日期查询开始时间
    - pageNum: 页码
    - pageSize: 每页页数
    - platform: 平台: 1.油葱商城 2.油葱健康 3.油葱学堂 4.荟友趣
    """

    url = "/mgmt/cms/channelLink/exportChannelLinkPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
