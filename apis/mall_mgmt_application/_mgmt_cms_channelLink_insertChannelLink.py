import os

from util.client import client

data = {
    "applyScene": 0,  # 适用场景 1.公众号 2.线下海报 3.线上活动
    "channelName": "",  # 渠道名称
    "pageId": 0,  # 跳转页面: 1：首页，2兑换中心，3完美时光荟活动、4新客专区、5丽龄专区、6丽龄3S随心礼活动、7抽奖活动、8拼图活动、9猜口令活动、10、油葱直播列表、11分享领券活动、12主题社群列表、13任务列表-我创建的主题社群、14任务列表-学习小组、15排行榜、16兴趣课程列表、17热门活动列表、18展业故事列表、19产品知识列表、20所有产品详情页、21所有课程详情页
    "platform": 0,  # 平台: 1.油葱商城 2.油葱健康 3.油葱学堂 4.荟友趣
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_channelLink_insertChannelLink(data=data, headers=headers):
    """
    渠道链接新增接口
    /mgmt/cms/channelLink/insertChannelLink

    参数说明:
    - applyScene: 适用场景 1.公众号 2.线下海报 3.线上活动
    - channelName: 渠道名称
    - pageId: 跳转页面: 1：首页，2兑换中心，3完美时光荟活动、4新客专区、5丽龄专区、6丽龄3S随心礼活动、7抽奖活动、8拼图活动、9猜口令活动、10、油葱直播列表、11分享领券活动、12主题社群列表、13任务列表-我创建的主题社群、14任务列表-学习小组、15排行榜、16兴趣课程列表、17热门活动列表、18展业故事列表、19产品知识列表、20所有产品详情页、21所有课程详情页
    - platform: 平台: 1.油葱商城 2.油葱健康 3.油葱学堂 4.荟友趣
    """

    url = "/mgmt/cms/channelLink/insertChannelLink"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
