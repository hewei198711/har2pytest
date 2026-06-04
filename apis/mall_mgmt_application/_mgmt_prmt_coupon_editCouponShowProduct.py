import os

from util.client import client

data = {
    "couponShowProducts": [],  # 优惠券卡片自定义关联商品集合
    "couponShowType": 0,  # 优惠券卡片推荐产品类型：0-默认，1-自定义关联
    "id": 0,  # 主键id：分享领券活动id 或 领券中心任务id
    "sourceType": 0,  # 配置来源入口:1-领券中心,2-分享领券(分享人),3-分享领券(助力人)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_editCouponShowProduct(data=data, headers=headers):
    """
    编辑优惠券自定义显示商品
    /mgmt/prmt/coupon/editCouponShowProduct

    参数说明:
    - couponShowProducts: 优惠券卡片自定义关联商品集合
    - couponShowType: 优惠券卡片推荐产品类型：0-默认，1-自定义关联
    - id: 主键id：分享领券活动id 或 领券中心任务id
    - sourceType: 配置来源入口:1-领券中心,2-分享领券(分享人),3-分享领券(助力人)
    """

    url = "/mgmt/prmt/coupon/editCouponShowProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
