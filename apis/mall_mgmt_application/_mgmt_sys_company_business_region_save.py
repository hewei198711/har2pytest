import os

from util.client import client

data = {
    "bindCodeList": [],  # 待绑定的地区编码集合
    "companyId": 0,  # 分公司id
    "regionLevel": 0,  # 地区等级:1->省、自治区、直辖市 2->地级市、地区、自治州、盟 3->市辖区、县级市、县 4-> 乡、镇
    "untieCodeList": [],  # 待解绑的地区编码集合
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_company_business_region_save(data=data, headers=headers):
    """
    保存公司业务范围信息
    /mgmt/sys/company/business/region/save

    参数说明:
    - bindCodeList: 待绑定的地区编码集合
    - companyId: 分公司id
    - regionLevel: 地区等级:1->省、自治区、直辖市 2->地级市、地区、自治州、盟 3->市辖区、县级市、县 4-> 乡、镇
    - untieCodeList: 待解绑的地区编码集合
    """

    url = "/mgmt/sys/company/business/region/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
