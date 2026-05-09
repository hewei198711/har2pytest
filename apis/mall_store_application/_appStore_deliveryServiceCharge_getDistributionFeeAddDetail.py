import os

from util.client import client

params = {
    "month": "",  # month
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_deliveryServiceCharge_getDistributionFeeAddDetail(params=params, headers=headers):
    """
    本期新增交付服务费明细列表
    /appStore/deliveryServiceCharge/getDistributionFeeAddDetail

    参数说明:
    - month: month
    """

    url = "/appStore/deliveryServiceCharge/getDistributionFeeAddDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
