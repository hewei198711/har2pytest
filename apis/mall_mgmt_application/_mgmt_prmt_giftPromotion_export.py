import os

from util.client import client

params = {
    "createTimeMax": "",  # 创建时间末, 格式：yyyy-MM-dd 23:59:59
    "createTimeMin": "",  # 创建时间始, 格式：yyyy-MM-dd 00:00:00
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "periodTimeMax": "",  # 活动有效期末, 格式：yyyy-MM-dd 23:59:59
    "periodTimeMin": "",  # 活动有效期始, 格式：yyyy-MM-dd 00:00:00
    "precisePromotionCode": 0,  # 是否精确查询活动编号：0-否 1-是
    "promotionCode": "",  # 活动编号
    "promotionName": "",  # 活动名称
    "promotionState": 0,  # 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿,不传表示查询全部
    "promotionStateList": [],  # 活动状态集合:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿,不传表示查询全部
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_giftPromotion_export(params=params, headers=headers):
    """
    导出赠品兑换活动
    /mgmt/prmt/giftPromotion/export

    参数说明:
    - createTimeMax: 创建时间末, 格式：yyyy-MM-dd 23:59:59
    - createTimeMin: 创建时间始, 格式：yyyy-MM-dd 00:00:00
    - pageNum: 当前页
    - pageSize: 每页数量
    - periodTimeMax: 活动有效期末, 格式：yyyy-MM-dd 23:59:59
    - periodTimeMin: 活动有效期始, 格式：yyyy-MM-dd 00:00:00
    - precisePromotionCode: 是否精确查询活动编号：0-否 1-是
    - promotionCode: 活动编号
    - promotionName: 活动名称
    - promotionState: 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿,不传表示查询全部
    - promotionStateList: 活动状态集合:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿,不传表示查询全部
    """

    url = "/mgmt/prmt/giftPromotion/export"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
