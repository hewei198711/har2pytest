import os

from util.client import client

data = {
    "codeEndTime": "",  # 兑换码失效时间 (null不限)
    "codeStartTime": "",  # 兑换码生效时间
    "endTime": "",  # 活动结束时间 (null不限)
    "generateCode": False,  # 是否生成兑换码 true:生成  false:不生成
    "id": 0,  # 主键
    "limitCount": 0,  # 可获得数量 (null不限)
    "promotionCode": "",  # 活动编号
    "promotionName": "",  # 活动名称
    "promotionState": 0,  # 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    "remarks": "",  # 赠品券说明
    "serialNo": "",  # 产品编码
    "sourceDesc": "",  # 赠品来源
    "startTime": "",  # 活动开始时间
    "total": 0,  # 赠品兑换码总量:-1不限量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_giftPromotion_edit(data=data, headers=headers):
    """
    编辑赠品活动
    /mgmt/prmt/giftPromotion/edit

    参数说明:
    - codeEndTime: 兑换码失效时间 (null不限)
    - codeStartTime: 兑换码生效时间
    - endTime: 活动结束时间 (null不限)
    - generateCode: 是否生成兑换码 true:生成  false:不生成
    - id: 主键
    - limitCount: 可获得数量 (null不限)
    - promotionCode: 活动编号
    - promotionName: 活动名称
    - promotionState: 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    - remarks: 赠品券说明
    - serialNo: 产品编码
    - sourceDesc: 赠品来源
    - startTime: 活动开始时间
    - total: 赠品兑换码总量:-1不限量
    """

    url = "/mgmt/prmt/giftPromotion/edit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
