import copy
from collections import OrderedDict
from flask import g, session
from applications.schemas import PowerOutSchema,PowerOutSchema2


#----------------------------------------------------
'''授权权限路由存入 session'''
def add_auth_session(current):
    role = current.role
    user_power = []
    for i in role:
        if i.enable == 0:
            continue
        for p in i.power:
            if p.enable == 0:
                continue
            user_power.append(p.code)
    return user_power
    # session['permissions'] = user_power
#----------------------------------------------------
    





#----------------------------------------------------
'''生成用户自己的菜单树'''
def make_menu_tree():
    role = g.user.role
    powers = []
    
    for i in role:
        # 如果角色没有被启用就直接跳过
        if i.enable == 0:
            continue
        # 如果存在权限
        if len(i.power) > 0:
        # 变量角色用户的权限
            for p in i.power:
                # 如果权限关闭了就直接跳过
                if p.enable == 0:
                    continue
                # 一二级菜单.不包含权限按钮
                if int(p.type) == 0 or int(p.type) == 1:
                    powers.append(p)
    # print(powers)
    power_schema = PowerOutSchema(many=True)  # 用已继承 ma.ModelSchema 类的自定制类生成序列化类
    power_dict = power_schema.dump(powers)    # 生成可序列化对象
    power_dict.sort(key=lambda x: x['sort'], reverse=True)
    # print(power_dict)


    menu = {
        "pages": [
            {
                "children": [
                    {
                        "id": 9999,
                        "parent_id": None,
                        "label": "首页",
                        "icon": "fa fa-cube",
                        "sort": 9999,
                        "url": "/",
                        "schema": {
                            "type": "page",
                            "title": "Home",
                            "body": "Home"
                        },
                    },
                ]
            }
        ]
    }

    menu_list = menu["pages"][0]["children"]
    for p in power_dict:
        if int(p['type']) == 0:
            menu_list.append({"label": p['name'], "icon": p['icon'], 'parent_id': p['parent_id'], 'sort': p['sort'], 'id': p['id']})
        else:
            menu_list.append({"label": p['name'], "icon": p['icon'], "url": p['url'], "schemaApi": p['url'], "parent_id": p['parent_id'], 'sort': p['sort'], 'id': p['id']})


    # 再重新赋值
    menu["pages"][0]["children"] = getTree(menu_list)
    return menu

#----------------------------------------------------







#----------------------------------------------------
'''权限管理生成菜单树'''
def getTree(menu_list):
    # print("="*50)
    # print(menu_list)
    # print("="*50)
    # 处理数据
    menu_map = {}
    for item in menu_list:
        item["children"] = []
        menu_map[item["id"]] = item

    tree = []
    for item in menu_map.values():
        if menu_map.get(item["parent_id"]): # 找儿子
            menu_map[item["parent_id"]]["children"].append(item)
            menu_map[item["parent_id"]]["children"].sort(key=lambda x: x['sort'], reverse=True)
        else: # 找出所有的顶级
            tree.append(item)
    
        
    tree.sort(key=lambda x: x['sort'], reverse=True)

    return tree



#----------------------------------------------------