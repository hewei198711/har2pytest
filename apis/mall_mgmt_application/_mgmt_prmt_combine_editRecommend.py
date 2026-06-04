import os

from util.client import client

data = {
    "combineRecommends": [
        {
            "cover": "",
            "id": 0,
            "name": "",
            "promotionId": 0,
            "recommendProducts": [
                {"groupType": 0, "productGroupIndex": 0, "productName": "", "quantity": 0, "serialNo": ""}
            ],
            "sort": 0,
        }
    ],  # 推荐组合信息
    "giftSteps": [{"limitMaxGiftNum": 0, "step": 0, "stepValue": 0.0}],  # 赠品阶梯配置对象集合
    "gifts": [
        {"customPrice": 0.0, "giveStage": "", "quantity": 0, "serialNo": "", "step": 0, "type": 0}
    ],  # 赠品池商品信息
    "id": 0,  # 活动id
    "products": [
        {
            "limitNum": 0,
            "openSelect": False,
            "productGroupIndex": 0,
            "productGroupName": "",
            "productGroupRemark": "",
            "serialNo": "",
            "sort": 0,
        }
    ],  # 主商品池信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_combine_editRecommend(data=data, headers=headers):
    """
    详情页编辑or新增推荐组合
    /mgmt/prmt/combine/editRecommend

    参数说明:
    - combineRecommends: 推荐组合信息
    - combineRecommends.cover: 推荐组合图片
    - combineRecommends.id: 推荐组合主键id
    - combineRecommends.name: 组合名称
    - combineRecommends.promotionId: 活动id
    - combineRecommends.recommendProducts: 推荐组合商品
    - combineRecommends.recommendProducts.groupType: 产品池类型: 0-主商品池 1-赠品池
    - combineRecommends.recommendProducts.productGroupIndex: 主产品池序号(赠品池为空)
    - combineRecommends.recommendProducts.productName: 产品名称
    - combineRecommends.recommendProducts.quantity: 推荐数量
    - combineRecommends.recommendProducts.serialNo: 产品编码
    - combineRecommends.sort: 排序
    - giftSteps: 赠品阶梯配置对象集合
    - giftSteps.limitMaxGiftNum: 赠品限制购买总数量
    - giftSteps.step: 阶梯
    - giftSteps.stepValue: 阶梯值(订单金额 或 PV)
    - gifts: 赠品池商品信息
    - gifts.customPrice: 画线价
    - gifts.giveStage: 赠送期数
    - gifts.quantity: 赠送数量
    - gifts.serialNo: 赠品产品编码
    - gifts.step: 赠品所属阶梯档位(固定商品无阶梯)
    - gifts.type: 赠品对应的组合类型:0-固定组合赠品,1-自由组合赠品
    - id: 活动id
    - products: 主商品池信息
    - products.limitNum: 最大购买数量
    - products.openSelect: 是否开启前端搜索: false-否 true-是
    - products.productGroupIndex: 主产品池序号
    - products.productGroupName: 主产品池名称
    - products.productGroupRemark: 主产品池说明
    - products.serialNo: 商品编码
    - products.sort: 排序
    """

    url = "/mgmt/prmt/combine/editRecommend"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
