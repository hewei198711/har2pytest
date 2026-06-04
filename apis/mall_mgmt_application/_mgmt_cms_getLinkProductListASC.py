import os

from util.client import client

params = {
    "decorateId": 0,  # 装修ID
    "decorateIdList": [],  # 装修ID列表
    "decorateType": 0,  # 装修类型（1:专题页,2:楼层页,3:热词,4:推荐商品,5,活动,6.Banner,7.app广告页,8.首页icon,9.素材详情页,10.魔法首页模块内容,11.魔法首页图片热区）
    "isFilterSecKill": False,  # 是否过滤秒杀活动: true 过滤秒杀活动
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getLinkProductListASC(params=params, headers=headers):
    """
    获取关联产品列表(升序)
    /mgmt/cms/getLinkProductListASC

    参数说明:
    - decorateId: 装修ID
    - decorateIdList: 装修ID列表
    - decorateType: 装修类型（1:专题页,2:楼层页,3:热词,4:推荐商品,5,活动,6.Banner,7.app广告页,8.首页icon,9.素材详情页,10.魔法首页模块内容,11.魔法首页图片热区）
    - isFilterSecKill: 是否过滤秒杀活动: true 过滤秒杀活动
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/mgmt/cms/getLinkProductListASC"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
