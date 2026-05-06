from util.client import client

params = {
    "orderNo": "EX914008260407000003",  # orderNo
}

headers = {"channel": "pc", "client": "op", "authorization": "请输入认证令牌"}


def _user_mgmt_order_detail(params=params, headers=headers):
    """
    订单详情
    /user/mgmt/order/detail

    参数说明:
    - orderNo: orderNo
    """

    url = "/user/mgmt/order/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
