
# g.permissions = ['admin:role:show','admin:role:add','admin:role:edit','admin:role:del']

# # "hidden": "admin:user:deletea" not in permission
api = {
  'list':          {'method': 'get',     'url': '/admin/role/list'       ,  'permission': 'admin:role:list'   },
  'show':          {'method': 'get',     'url': '/admin/role/$id'        ,  'permission': 'admin:role:show'   },
  'add':           {'method': 'post',    'url': '/admin/role'            ,  'permission': 'admin:role:add'    },
  'edit':          {'method': 'put',     'url': '/admin/role/$id'        ,  'permission': 'admin:role:edit'   },
  'switch':        {'method': 'put',     'url': '/admin/role/status/$id' ,  'permission': 'admin:role:edit' },
  'del':           {'method': 'delete',  'url': '/admin/role/$id'        ,  'permission': 'admin:role:del'    },
  'bindPowerEdit': {'method': 'post',    'url': '/admin/role/power/$id'  ,  'permission': 'admin:role:edit'   },
  'bindPowerShow': {'method': 'get',     'url': '/admin/power'           ,  'permission': 'admin:power:list'  },
}


def getRoleJson(val):
  permissions = val


  roleJson = {
    "type": "page",
    # "title": "角色管理",
    "body": [
      {
        "type": "flex",
        "className": "p-1",
        "items": [
          {
            "type": "wrapper",
            "body": [
              {
                "type": "crud",
                "syncLocation": False,
                "api": {
                  "method": api['list']['method'],
                  "url": api['list']['url'],
                },
                "bulkActions": [
                ],
                "itemActions": [
                ],
                "features": [
                  "create",
                  "update",
                  "delete"
                ],
                "filterColumnCount": 3,
                "headerToolbar": [
                  {
                    "label": "新增",
                    "type": "button",
                    "icon": "fa-plus",
                    "actionType": "dialog",
                    "level": "primary",
                    "hidden": api['add']['permission'] not in permissions,
                    "dialog": {
                      "title": "新增",
                      "body": {
                        "type": "form",
                        "api": {
                          "method": api['add']['method'],
                          "url": api['add']['url'],
                        },
                        "body": [
                          {
                            "type": "input-text",
                            "name": "roleName",
                            "label": "角色名称",
                            "required": True,
                          },
                          {
                            "type": "input-text",
                            "name": "roleCode",
                            "label": "角色标识",
                            "required": True,
                          },
                          {
                            "type": "switch",
                            "name": "enable",
                            "label": "是否启用",
                            "falseValue": '0',
                            "trueValue": '1',
                            "onText": "已启用",
                            "offText": "已禁用"
                          },
                          {
                            "type": "native-number",
                            "name": "sort",
                            "label": "排序",
                            "required": True,
                          },
                          {
                            "type": "input-text",
                            "name": "details",
                            "label": "详情",
                          }
                        ]
                      }
                    },
                    "id": "u:02c2a57f01cd",
                    "align": "left",
                  },
                  {
                    "type": "columns-toggler",
                    "align": "right"
                  },
                  {
                    "type": "export-excel",
                    "tpl": "内容",
                    "id": "u:adc705a92fe1",
                    "align": "right"
                  },
                  {
                    "type": "button",
                    "tpl": "内容",
                    "id": "u:cd225012cef1",
                    "align": "right",
                    "label": "刷新",
                    "onEvent": {
                      "click": {
                        "actions": [
                          {
                            "args": {
                              "resetPage": False
                            },
                            "actionType": "reload",
                            "componentId": "u:e493e7bd7903",
                            "data": None
                          }
                        ],
                        "weight": 0
                      }
                    }
                  },
                                  {
                          "type": "search-box",
                          "align": "right",
                          "name": "search",
                          "placeholder": "请输入用户名",
                          "mini": True,
                          "addOn": {
                                  "label": "搜索",
                                  "type": "submit"
                          }
                  },
                ],
                "id": "u:e493e7bd7903",
                "perPageAvailable": [
                  10,
                  50,
                  100,
                  200,
                  500
                ],
                "messages": {
                },
                "mode": "table",
                "columns": [
                  {
                    "name": "id",
                    "label": "ID",
                    "type": "text",
                  },
                  {
                    "name": "roleName",
                    "label": "角色名称",
                    "type": "text",
                  },
                  {
                    "type": "text",
                    "name": "roleCode",
                    "label": "角色标识",
                  },
                  {
                    "type": "switch",
                    "name": "enable",
                    "label": "启用",
                    "falseValue": '0',
                    "trueValue": '1',
                    "onText": "已启用",
                    "offText": "已禁用",
                    "disabled": api['switch']['permission'] not in permissions,
                    "onEvent": {
                        "change": {
                          "actions": [
                            {
                              "actionType": "ajax",
                              "args": {
                                "api": {
                                  "url": api['switch']['url'],
                                  "method": api['switch']['method']
                                },
                              },
                              "data": {
                                "enable": "$enable"
                              }
                            },
                          ]
                        }
                    }
                  },
                  {
                    "type": "text",
                    "name": "sort",
                    "label": "排序",
                  },
                  {
                    "type": "text",
                    "name": "details",
                    "label": "详情",
                  },
                  {
                    "type": "date",
                    "name": "create_at",
                    "label": "创建时间",
                    "format": "YYYY-MM-DD HH:mm:ss"
                  },
                  {
                    "type": "date",
                    "name": "update_at",
                    "label": "修改时间",
                    "format": "YYYY-MM-DD HH:mm:ss"
                  },
                  {
                    "type": "operation",
                    "label": "操作",
                    "align": "center",
                    "fixed": "right",
                    "buttons": [
                      {
                        "label": "编辑",
                        "type": "button",
                        "actionType": "dialog",
                        "level": "link",
                        "hidden": api['edit']['permission']  not in permissions,
                        "dialog": {
                          "title": "编辑",
                          "body": {
                            "type": "form",
                            "api":  {
                              "method": api['edit']['method'],
                              "url": api['edit']['url']
                            },
                            "body": [
                                {
                                  "type": "input-text",
                                  "name": "roleName",
                                  "label": "角色名称",
                                  "required": True,
                                },
                                {
                                  "type": "input-text",
                                  "name": "roleCode",
                                  "label": "角色标识",
                                  "required": True,
                                },
                                {
                                  "type": "switch",
                                  "name": "enable",
                                  "label": "是否启用",
                                  "falseValue": '0',
                                  "trueValue": '1',
                                  "onText": "已启用",
                                  "offText": "已禁用"
                                },
                                {
                                  "type": "native-number",
                                  "name": "sort",
                                  "label": "排序",
                                  "required": True,
                                },
                                {
                                  "type": "input-text",
                                  "name": "details",
                                  "label": "详情",
                                }
                            ]
                          }
                        },
                      },
                      {
                        "label": "权限",
                        "type": "button",
                        "actionType": "dialog",
                        "level": "link",
                        "dialog": {
                          "title": "权限",
                          "body": {
                            "type": "form",
                            # "debug": True,
                            # 权限编辑初始化，获取当前角色的权限
                            # "initApi": {
                            #     "method": "get",
                            #     "url": "/admin/role/power/$id",
                            # },
                            # 表单提交
                            "api":  {
                              "method": api['bindPowerEdit']['method'],
                              "url": api['bindPowerEdit']['url'],
                            },
                            "body": [
                              {
                                "type": "input-tree",
                                "name": "ids",
                                # "value": "1",
                                # "source": "/api/v1/permission",
                                "multiple": True,
                                "extractValue": True,
                                "joinValues": False,
                                "autoCheckChildren": False,
                                "initiallyOpen": True,
                                "size": "full",
                                "showIcon": True,
                                "treeContainerClassName": "no-border",
                                "size": "lg",
                                "mode": "inline",
                                "value": "${power|pick:id}",
                                "source": {
                                    "method": api['bindPowerShow']['method'],
                                    "url": api['bindPowerShow']['url'],
                                    # "responseData": {
                                    #   "options": "${rows|pick:label~name,value~id,children~children}"
                                    # }
                                  },
                                # "options": [
                                  # {
                                  #   "label": "B",
                                  #   "value": "b",
                                  #   "children": [
                                  #     {
                                  #       "label": "B-1",
                                  #       "value": "b-1"
                                  #     },
                                  #     {
                                  #       "label": "B-2",
                                  #       "value": "b-2"
                                  #     },
                                  #     {
                                  #       "label": "B-3",
                                  #       "value": "b-3"
                                  #     }
                                  #   ]
                                  # },
                                  # {
                                  #   "label": "C",
                                  #   "value": "c"
                                  # }
                                # ]
                              }
                            ]
                          }
                        }
                      },
                      {
                        "type": "button",
                        "label": "删除",
                        "actionType": "ajax",
                        "level": "link",
                        "className": "text-danger",
                        "confirmText": "确定要删除 $roleName ？",
                        "hidden": api['del']['permission'] not in permissions,
                        "api": {
                          "method":  api['del']['method'],
                          "url":  api['del']['url']
                        },
                      }
                    ],
                  }
                ],

                "hideQuickSaveBtn": False,
                "alwaysShowPagination": True,
                "footerToolbar": [
                  {
                    "type": "statistics",
                    "align": "left"
                  },
                  {
                    "type": "pagination",
                    "align": "right"
                  },
                  {
                    "type": "switch-per-page",
                    "tpl": "内容",
                    "id": "u:631f29b5c989",
                    "align": "left"
                  }
                ],
                "bodyClassName": "",
                "className": "p-l-sm p-r-sm",
                "pageField": "page",
                "perPageField": "perPage",
                "autoJumpToTopOnPagerChange": True,
                "syncResponse2Query": True,
                "orderField": "od",
                "perPage": 10
              }
            ],
            "size": "md",
            "style": {
              "position": "static",
              "display": "block",
              "flex": "1 1 auto",
              "flexGrow": 1,
              "flexBasis": "auto",
              "flexWrap": "nowrap",
              "boxShadow": "2px 2px 2px 3px #f3ecec",
              "backgroundSize": "",
              "backgroundPosition": "",
              "backgroundColor": "",
              "backgroundImage": "",
              "borderLeftStyle": "",
              "borderTopStyle": "",
              "borderRightStyle": "",
              "borderBottomStyle": ""
            },
            "isFixedHeight": False,
            "isFixedWidth": False,
          }
        ],
        "style": {
          "position": "static"
        },
        "direction": "row",
        "justify": "flex-start",
        "alignItems": "stretch",
      }
    ],
  }


  return roleJson