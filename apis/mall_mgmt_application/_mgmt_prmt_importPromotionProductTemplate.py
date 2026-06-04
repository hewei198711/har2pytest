import os

from util.client import client

params = {
    "exchangeType": "",  # 换购类型1产品换购2PV达标换购3数量达标换购4金额达标换购
    "pointSteps": "",  # 阶梯集合
    "promotionType": "",  # 活动类型1活动2换购3预售
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_importPromotionProductTemplate(params=params, headers=headers):
    """
    导入活动产品模板下载
    /mgmt/prmt/importPromotionProductTemplate

    参数说明:
    - exchangeType: 换购类型1产品换购2PV达标换购3数量达标换购4金额达标换购
    - pointSteps: 阶梯集合
    - promotionType: 活动类型1活动2换购3预售
    """

    url = "/mgmt/prmt/importPromotionProductTemplate"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
