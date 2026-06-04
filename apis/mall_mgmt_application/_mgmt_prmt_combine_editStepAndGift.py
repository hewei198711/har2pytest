import os

from util.client import client

data = {
    "giftSteps": [{"limitMaxGiftNum": 0, "step": 0, "stepValue": 0.0}],  # 赠品阶梯配置对象集合
    "gifts": [
        {"customPrice": 0.0, "giveStage": "", "quantity": 0, "serialNo": "", "step": 0, "type": 0}
    ],  # 赠品池商品集合
    "promotionId": 0,  # 活动id
    "steps": [{"customPrice": 0.0, "step": 0}],  # 阶梯信息集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_combine_editStepAndGift(data=data, headers=headers):
    """
    详情页编辑阶梯-阶梯商品-赠品
    /mgmt/prmt/combine/editStepAndGift

    参数说明:
    - giftSteps: 赠品阶梯配置对象集合
    - giftSteps.limitMaxGiftNum: 赠品限制购买总数量
    - giftSteps.step: 阶梯
    - giftSteps.stepValue: 阶梯值(订单金额 或 PV)
    - gifts: 赠品池商品集合
    - gifts.customPrice: 画线价
    - gifts.giveStage: 赠送期数
    - gifts.quantity: 赠送数量
    - gifts.serialNo: 赠品产品编码
    - gifts.step: 赠品所属阶梯档位(固定商品无阶梯)
    - gifts.type: 赠品对应的组合类型:0-固定组合赠品,1-自由组合赠品
    - promotionId: 活动id
    - steps: 阶梯信息集合
    - steps.customPrice: 价格
    - steps.step: 阶梯档位
    """

    url = "/mgmt/prmt/combine/editStepAndGift"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
