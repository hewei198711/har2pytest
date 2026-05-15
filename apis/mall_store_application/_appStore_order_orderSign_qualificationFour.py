import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
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
    "promotionId": 0,  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_orderSign_qualificationFour(data=data, headers=headers):
    """
    查询用户是否有签约购4.0活动资格
    /appStore/order/orderSign/qualificationFour

    参数说明:
    - cardNo: 会员卡号
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
    - promotionId: 活动id
    """

    url = "/appStore/order/orderSign/qualificationFour"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
