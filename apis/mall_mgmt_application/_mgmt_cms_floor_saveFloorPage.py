import os

from util.client import client

data = {
    "activityId": "",  # 关联的活动id(签约购)
    "appImg": "",  # APP端图片
    "descript": "",  # 描述
    "linkProductType": 0,  # 关联商品类型:1.关联商品列表 2.关联日销量top20 3.关联周销量top20 4.关联月销量top20
    "linkUrl": "",  # 广告图片跳转URL
    "mpImg": "",  # 小程序图片地址
    "name": "",  # 楼层菜单名称
    "pcImg": "",  # PC端图片
    "productList": [{"serialNo": "", "sort": 0}],  # 关联的产品列表
    "relateType": 0,  # 关联类型,0：不设置，3:商城内部链接或外部链接，4:关联签约购活动
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_floor_saveFloorPage(data=data, headers=headers):
    """
    新增楼层页
    /mgmt/cms/floor/saveFloorPage

    参数说明:
    - activityId: 关联的活动id(签约购)
    - appImg: APP端图片
    - descript: 描述
    - linkProductType: 关联商品类型:1.关联商品列表 2.关联日销量top20 3.关联周销量top20 4.关联月销量top20
    - linkUrl: 广告图片跳转URL
    - mpImg: 小程序图片地址
    - name: 楼层菜单名称
    - pcImg: PC端图片
    - productList: 关联的产品列表
    - productList.serialNo: 产品编码
    - productList.sort: sort
    - relateType: 关联类型,0：不设置，3:商城内部链接或外部链接，4:关联签约购活动
    - sort: 排序
    """

    url = "/mgmt/cms/floor/saveFloorPage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
