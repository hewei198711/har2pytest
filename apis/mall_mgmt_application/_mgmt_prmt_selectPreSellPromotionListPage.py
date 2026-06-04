import os

from util.client import client

params = {
    "createTimeMax": "",  # 创建时间大
    "createTimeMin": "",  # 创建时间小
    "exchangeType": 0,  # 换购类型1产品换购2PV达标换购3数量达标换购4金额达标换购
    "limitType": 0,  # 限购方式1不限量2独立限量3统一限量4按需导入5按阶梯配置独立限量6按阶梯配置统一限量
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "periodTimeMax": "",  # 活动有效期大
    "periodTimeMin": "",  # 活动有效期小
    "promotionCode": "",  # 活动编码
    "promotionIds": [],  # 活动id集合
    "promotionName": "",  # 活动名称
    "promotionState": 0,  # 活动状态1待审核2待开始3进行中4已结束5已驳回6草稿7支付定金阶段8支付尾款阶段
    "promotionStates": [],  # 活动状态集合:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    "promotionType": 0,  # 活动类型:1-活动,2-换购,4-预售
    "promotionTypeExt": 0,  # 基于抢购活动(promotionType=1)类型区分：0-原抢购(秒杀) 1-常规
    "serialNo": "",  # 商品编码
    "states": [],  # 活动状态集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_selectPreSellPromotionListPage(params=params, headers=headers):
    """
    预售活动分页列表查询
    /mgmt/prmt/selectPreSellPromotionListPage

    参数说明:
    - createTimeMax: 创建时间大
    - createTimeMin: 创建时间小
    - exchangeType: 换购类型1产品换购2PV达标换购3数量达标换购4金额达标换购
    - limitType: 限购方式1不限量2独立限量3统一限量4按需导入5按阶梯配置独立限量6按阶梯配置统一限量
    - pageNum: 当前页
    - pageSize: 每页数量
    - periodTimeMax: 活动有效期大
    - periodTimeMin: 活动有效期小
    - promotionCode: 活动编码
    - promotionIds: 活动id集合
    - promotionName: 活动名称
    - promotionState: 活动状态1待审核2待开始3进行中4已结束5已驳回6草稿7支付定金阶段8支付尾款阶段
    - promotionStates: 活动状态集合:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    - promotionType: 活动类型:1-活动,2-换购,4-预售
    - promotionTypeExt: 基于抢购活动(promotionType=1)类型区分：0-原抢购(秒杀) 1-常规
    - serialNo: 商品编码
    - states: 活动状态集合
    """

    url = "/mgmt/prmt/selectPreSellPromotionListPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
