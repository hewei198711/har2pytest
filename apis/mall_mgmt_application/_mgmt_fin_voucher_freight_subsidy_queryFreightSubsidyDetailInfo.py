import os
from urllib.parse import urlencode

from util.client import client

data = {
    "grantdtlId": 0,  # 运费补贴券发放id号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_voucher_freight_subsidy_queryFreightSubsidyDetailInfo(data=data, headers=headers):
    """
    运费补贴券管理界面查询详情接口（商城后台）
    /mgmt/fin/voucher/freight/subsidy/queryFreightSubsidyDetailInfo

    参数说明:
    - grantdtlId: 运费补贴券发放id号
    """

    url = "/mgmt/fin/voucher/freight/subsidy/queryFreightSubsidyDetailInfo"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
