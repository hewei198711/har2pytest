import os

from util.client import client

data = {
    "customerCard": "",  # 给某个顾客下单的会员卡号
    "orderNo": "",  # 订单编号
    "productList": [
        {
            "cusSerialNo": "",
            "exchangeParam": {"exchangeSerialNo": "", "number": 0},
            "number": 0,
            "prodType": 0,
            "productGroupIndex": 0,
            "serialNo": "",
            "sssProdType": 0,
        }
    ],  # 购买产品信息
    "promotionId": 0,  # 活动ID
    "signType": 0,  # 签约类型，1：2.0；2：3.0；3：4.0
    "sourceType": 0,  # 0(立即购买),1(快速购货),2(购物车提交),3(结算前销售调整),4(定制商品购买),5(辅销品购买),6(旧版商品购买),7(调差购买),8(85折转分订单),9(85折转分补报订单),10(单位团购报单)
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_getCouponList(data=data, headers=headers):
    """
    获取选中结算分组的可用和不可用优惠券列表
    /appStore/order/orderSign/getCouponList

    参数说明:
    - customerCard: 给某个顾客下单的会员卡号
    - orderNo: 订单编号
    - productList: 购买产品信息
    - productList.cusSerialNo: 定制商品二级编码,购买定制商品不能为空
    - productList.exchangeParam: 换购商品信息
    - productList.exchangeParam.exchangeSerialNo: 换购商品编码
    - productList.exchangeParam.number: 换购商品数量
    - productList.number: 产品数量
    - productList.prodType: 签约购3.0使用，1：必选产品；2：可选产品
    - productList.productGroupIndex: 随心购主产品分组序号
    - productList.serialNo: 产品编码
    - productList.sssProdType: S+S+S使用，1：主产品；2：赠品
    - promotionId: 活动ID
    - signType: 签约类型，1：2.0；2：3.0；3：4.0
    - sourceType: 0(立即购买),1(快速购货),2(购物车提交),3(结算前销售调整),4(定制商品购买),5(辅销品购买),6(旧版商品购买),7(调差购买),8(85折转分订单),9(85折转分补报订单),10(单位团购报单)
    - storeCode: 服务中心编码
    """

    url = "/appStore/order/orderSign/getCouponList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
