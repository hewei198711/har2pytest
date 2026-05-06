from util.client import client

data = {
    "orderNo": "EX914008260407000003",  # 兑换流水号
    "returnReason": "111111",  # 退货原因
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": "请输入认证令牌",
}


def _user_mgmt_order_return_submit(data=data, headers=headers):
    """
    提交售后
    /user/mgmt/order/return/submit

    参数说明:
    - req: req
    - orderNo: 兑换流水号
    - returnReason: 退货原因
    """

    url = "/user/mgmt/order/return/submit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
