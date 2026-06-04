import os

from util.client import client

params = {
    "couponIds": [],  # TODO: 添加参数说明
    "couponName": "",  # 优惠券名称
    "couponNumber": "",  # 编号
    "couponNumberPreciseQuery": "",  # 优惠券编号精确查询
    "couponState": 0,  # 状态1待审核2待生效3生效中4已失效5已禁用6已驳回7草稿
    "couponStateList": [],  # 查询优惠券状态集合 1-待审核 2-待生效 3-生效中 4-已失效 5-已禁用 6-已驳回 7-草稿
    "createTimeMax": "",  # 创建时间大
    "createTimeMin": "",  # 创建时间小
    "endTime": "",  # 结束时间
    "isAccurateSearch": 0,  # 是否精确搜索:0否:1是
    "isGenerateCode": 0,  # 是否生成优惠码0不生成1生成
    "limitStore": 0,  # 是否限制门店0否1是2限代购
    "limitStoreList": [],  # 是否限制门店0否1是2限代购
    "orderWayList": [],  # 下单限制1自购2代购
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "platforms": [],  # 限制平台结果累加1app2pc4小程序
    "startTime": "",  # 开始时间
    "startType": 0,  # 开始生效方式1定时生效2派发后生效
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_getCouponPage(params=params, headers=headers):
    """
    分页获取优惠券列表
    /mgmt/prmt/loginGift/getCouponPage

    参数说明:
    - couponName: 优惠券名称
    - couponNumber: 编号
    - couponNumberPreciseQuery: 优惠券编号精确查询
    - couponState: 状态1待审核2待生效3生效中4已失效5已禁用6已驳回7草稿
    - couponStateList: 查询优惠券状态集合 1-待审核 2-待生效 3-生效中 4-已失效 5-已禁用 6-已驳回 7-草稿
    - createTimeMax: 创建时间大
    - createTimeMin: 创建时间小
    - endTime: 结束时间
    - isAccurateSearch: 是否精确搜索:0否:1是
    - isGenerateCode: 是否生成优惠码0不生成1生成
    - limitStore: 是否限制门店0否1是2限代购
    - limitStoreList: 是否限制门店0否1是2限代购
    - orderWayList: 下单限制1自购2代购
    - pageNum: 当前页
    - pageSize: 每页数量
    - platforms: 限制平台结果累加1app2pc4小程序
    - startTime: 开始时间
    - startType: 开始生效方式1定时生效2派发后生效
    """

    url = "/mgmt/prmt/loginGift/getCouponPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
