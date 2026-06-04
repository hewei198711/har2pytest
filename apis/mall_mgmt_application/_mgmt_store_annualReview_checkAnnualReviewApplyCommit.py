import os

from util.client import client

params = {
    "reviewModelType": 0,  # 年审类型 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审
    "reviewTitle": "",  # 年审标题
    "storeCode": "",  # 店铺编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_annualReview_checkAnnualReviewApplyCommit(params=params, headers=headers):
    """
    新增年审申请时的校验
    /mgmt/store/annualReview/checkAnnualReviewApplyCommit

    参数说明:
    - reviewModelType: 年审类型 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审
    - reviewTitle: 年审标题
    - storeCode: 店铺编号
    """

    url = "/mgmt/store/annualReview/checkAnnualReviewApplyCommit"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
