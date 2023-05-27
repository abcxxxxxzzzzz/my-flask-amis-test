# g.permissions = [
#   "admin:power:show",
#   "admin:power:add",
#   "admin:power:edit",
#   "admin:power:del"]

# # "hidden": "admin:user:deletea" not in permission
api = {
  "list":      {"method": "get",     "url": "/admin/power/list"        ,  'permission': 'admin:power:list'   },
  "show":      {"method": "get",     "url": "/admin/power/$id"         ,  'permission': 'admin:power:show'   },
  "add":       {"method": "post",    "url": "/admin/power"             ,  'permission': 'admin:power:add'   },
  "edit":      {"method": "put",     "url": "/admin/power/$id"         ,  'permission': 'admin:power:edit'   },
  "switch":    {"method": "put",     "url": "/admin/power/status/$id"  ,  'permission': 'admin:power:edit'   },
  "del":       {"method": "delete",  "url": "/admin/power/$id"         ,  'permission': 'admin:power:del'   },
}






def getPowerJson(val):
  permissions = val

  powerJson = {
    "type": "page",
    # "title": "权限管理",
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
                  "method": api["list"]["method"],
                  "url": api["list"]["url"]
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
                    "icon": "fas fa-plus",
                    "actionType": "dialog",
                    "level": "primary",
                    "hidden": api["add"]["permission"] not in permissions,
                    "dialog": {
                      "title": "新增",
                      "body": {
                        "type": "form",
                        "api": {
                          "method": api["add"]["method"],
                          "url": api["add"]["url"]
                        },
                        "body": [
                                {
                                    "type": "radios",
                                    "name": "type",
                                    "label": "类型",
                                    "required": True,
                                    "inline": True,
                                    "value": "0",
                                    "options": [
                                        {
                                            "label": "目录",
                                            "value": "0"
                                        },
                                        {
                                            "label": "菜单",
                                            "value": "1"
                                        },
                                        {
                                            "label": "按钮",
                                            "value": "2"
                                        }
                                    ]
                                    
                                },
                                {
                                  "name": "name",
                                  "label": "权限名称",
                                  "type": "input-text",
                                  "required": True,
                                },
                                {
                                  "type": "input-text",
                                  "name": "code",
                                  "label": "权限标识",
                                  "hiddenOn": "data.type == 0",
                                  "clearValueOnHidden": True,
                                  "required": True,
                                },
                                {
                                    "type": "select",
                                    "name": "open_type",
                                    "label": "请求方式",
                                    "required": True,
                                    "value": "",
                                    "hiddenOn": "data.type != 2",
                                    "clearValueOnHidden": True,
                                    "options": [
                                        {
                                            "label": "get",
                                            "value": "get"
                                        },
                                        {
                                            "label": "post",
                                            "value": "post"
                                        },
                                        {
                                            "label": "put",
                                            "value": "put"
                                        },
                                        {
                                            "label": "delete",
                                            "value": "delete"
                                        }
                                    ]
                                },
                                {
                                  "type": "input-text",
                                  "name": "url",
                                  "label": "权限路径",
                                  "hiddenOn": "data.type == 0",
                                  "clearValueOnHidden": True,
                                  "required": True,
                                },
                                {
                                  "type": "input-text",
                                  "name": "parent_id",
                                  "label": "父类编号",
                                  "hiddenOn": "data.type == 0",
                                  "clearValueOnHidden": True,
                                  "required": True,
                                },
                                {
                                  "type": "input-text",
                                  "name": "icon",
                                  "label": "图标",
                                  "hiddenOn": "data.type == 2",
                                  "required": True,
                                },
                                {
                                  "type": "native-number",
                                  "name": "sort",
                                  "label": "排序",
                                  "required": True,
                                },
                        ]
                      }
                    },
                    
                    "align": "left",
                  },
                  {
                    "type": "columns-toggler",
                    "align": "right"
                  },
                  {
                    "type": "export-excel",
                    "tpl": "内容",
                    
                    "align": "right"
                  },
                  {
                    "type": "button",
                    "tpl": "内容",
                    
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
                  }
                ],
                
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
                "footable": {
                  "expand": "all" # 展开
                },
                "columns": [
                  {
                    "name": "id",
                    "label": "权限编号",
                    "type": "text",
                  },
                  {
                    "type": "tpl",
                    "name": "icon",
                    "label": "图标",
                    "tpl": "<i class='${icon}'></i>"
                  },
                  {
                    "name": "name",
                    "label": "权限名称",
                    "type": "text",
                  },
                  {
                    # "type": "text",
                    "name": "type",
                    "label": "权限类型",
                    "type": "mapping",
                    "map": {
                        "0": "<span class=\"label label-info\">目录</span>",
                        "1": "<span class=\"label label-success\">菜单</span>",
                        "2": "<span class=\"label label-warning\">按钮</span>",
                        "*": "其他：${type}"
                    }
                  },
                  {
                    "type": "text",
                    "name": "code",
                    "label": "权限标识",
                  },
                  {
                    "type": "text",
                    "name": "url",
                    "label": "权限路径",
                  },
                  {
                    "name": "open_type",
                    "label": "请求方式",
                    "type": "mapping",
                    "map": {
                        "get": "<span class=\"label label-info\">GET</span>",
                        "post": "<span class=\"label label-success\">POST</span>",
                        "put": "<span class=\"label label-warning\">PUT</span>",
                        "delete": "<span class=\"label label-danger\">DELETE</span>",
                        "*": "其他：${type}"
                    }
                  },
                  {
                    "type": "text",
                    "name": "parent_id",
                    "label": "父类编号",
                  },
                  {
                    "type": "text",
                    "name": "sort",
                    "label": "排序",
                  },
                  {
                    "type": "switch",
                    "name": "enable",
                    "label": "是否启用",
                    "falseValue": "0",
                    "trueValue": "1",
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
                    "type": "date",
                    "name": "create_time",
                    "label": "创建时间",
                    "format": "YYYY-MM-DD HH:mm:ss"
                  },
                  {
                    "type": "date",
                    "name": "update_time",
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
                        "hidden": api["edit"]["permission"] not in permissions,
                        "level": "link",
                        "dialog": {
                          "title": "编辑",
                          "body": {
                            "type": "form",
                            "api": {
                              "method": api["edit"]["method"],
                              "url": api["edit"]["url"],
                            },
                            "body": [
                                  {
                                      "type": "radios",
                                      "name": "type",
                                      "label": "类型",
                                      "required": True,
                                      "inline": True,
                                      "value": "0",
                                      "options": [
                                          {
                                              "label": "目录",
                                              "value": "0"
                                          },
                                          {
                                              "label": "菜单",
                                              "value": "1"
                                          },
                                          {
                                              "label": "按钮",
                                              "value": "2"
                                          }
                                      ]
                                      
                                  },
                                  {
                                    "name": "name",
                                    "label": "权限名称",
                                    "type": "input-text",
                                    "required": True,
                                  },
                                  {
                                    "type": "input-text",
                                    "name": "code",
                                    "label": "权限标识",
                                    "hiddenOn": "data.type == 0",
                                    "clearValueOnHidden": True,
                                    "required": True,
                                  },
                                  {
                                      "type": "select",
                                      "name": "open_type",
                                      "label": "请求方式",
                                      "required": True,
                                      "value": "",
                                      "hiddenOn": "data.type != 2",
                                      "clearValueOnHidden": True,
                                      "options": [
                                          {
                                              "label": "get",
                                              "value": "get"
                                          },
                                          {
                                              "label": "post",
                                              "value": "post"
                                          },
                                          {
                                              "label": "put",
                                              "value": "put"
                                          },
                                          {
                                              "label": "delete",
                                              "value": "delete"
                                          }
                                      ]
                                  },
                                  {
                                    "type": "input-text",
                                    "name": "url",
                                    "label": "权限路径",
                                    "hiddenOn": "data.type == 0",
                                    "clearValueOnHidden": True,
                                    "required": True,
                                  },
                                  {
                                    "type": "input-text",
                                    "name": "parent_id",
                                    "label": "父类编号",
                                    "hiddenOn": "data.type == 0",
                                    "clearValueOnHidden": True,
                                    "required": True,
                                  },
                                  {
                                    "type": "input-text",
                                    "name": "icon",
                                    "label": "图标",
                                    "hiddenOn": "data.type == 2",
                                    "required": True,
                                  },
                                  {
                                    "type": "native-number",
                                    "name": "sort",
                                    "label": "排序",
                                    "required": True,
                                  },
                          ]
                          }
                        },
                        
                      },
                      {
                        "type": "button",
                        "label": "删除",
                        "actionType": "ajax",
                        "level": "link",
                        "className": "text-danger",
                        "confirmText": "确定要删除 $name ？",
                        "hidden": api["del"]["permission"] not in permissions,
                        "api": {
                          "method": api["del"]["method"],
                          "url": api["del"]["url"]
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
                "perPage": 9999
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

  
  return powerJson
