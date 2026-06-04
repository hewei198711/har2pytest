import os

from util.client import client

data = {
    "annualReviewContent": "",  # 年审说明
    "annualReviewName": "",  # 年审模块名称
    "annualReviewTitle": "",  # 年审标题
    "annualReviewType": 0,  # 年审类型 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_annualReview_saveOrEdit(data=data, headers=headers):
    """
    年审模块配置新增/编辑
    /mgmt/store/annualReview/saveOrEdit

    参数说明:
    - annualReviewContent: 年审说明
    - annualReviewName: 年审模块名称
    - annualReviewTitle: 年审标题
    - annualReviewType: 年审类型 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审
    """

    url = "/mgmt/store/annualReview/saveOrEdit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
