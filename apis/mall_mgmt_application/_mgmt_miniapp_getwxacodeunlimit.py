import os

from util.client import client

data = {
    "page": "",  # 主页 例如 pages/index/index, 根路径前不要填加 /,不能携带参数（参数请放在scene字段里）
    "scene": "",  # 场景值
    "type": 0,  # 分享类型 1：直播 2：首页 3：邀请开卡 4:分享商品详情 5:acc清洗人员 6:素材分享 7:文档分享 8:优惠券转赠 9:分享登录提醒 10:分享领券 11:抽奖活动 12:生活社区 13:码上有名 14:扫码领券 15:签约购活动 16:代客选品 17-C端用户转赠优惠券18-随心购活动 19-魔法首页预览 20-魔法专区预览 21-签约购活动3.0 22-口令活动 23-线上答题 24-3S组合活动 25-签约购4.0 26.问卷 27-体验中心 28-拼图活动 29-送礼活动 30-渠道链接 31-公益购活动
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_miniapp_getwxacodeunlimit(data=data, headers=headers):
    """
    获取小程序太阳码（非登录不能获取）
    /mgmt/miniapp/getwxacodeunlimit

    参数说明:
    - page: 主页 例如 pages/index/index, 根路径前不要填加 /,不能携带参数（参数请放在scene字段里）
    - scene: 场景值
    - type: 分享类型 1：直播 2：首页 3：邀请开卡 4:分享商品详情 5:acc清洗人员 6:素材分享 7:文档分享 8:优惠券转赠 9:分享登录提醒 10:分享领券 11:抽奖活动 12:生活社区 13:码上有名 14:扫码领券 15:签约购活动 16:代客选品 17-C端用户转赠优惠券18-随心购活动 19-魔法首页预览 20-魔法专区预览 21-签约购活动3.0 22-口令活动 23-线上答题 24-3S组合活动 25-签约购4.0 26.问卷 27-体验中心 28-拼图活动 29-送礼活动 30-渠道链接 31-公益购活动
    """

    url = "/mgmt/miniapp/getwxacodeunlimit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
