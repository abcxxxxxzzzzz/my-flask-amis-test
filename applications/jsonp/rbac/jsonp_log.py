
# g.permissions = ['admin:role:show','admin:role:add','admin:role:edit','admin:role:del']

# # "hidden": "admin:user:deletea" not in permission
api = {
  'list':          {'method': 'get',       'url': '/admin/log/list'      ,  'permission': 'admin:log:list'   },
  'batchDel':      {'method': 'delete',    'url': '/admin/log/batch/$ids',  'permission': 'admin:log:batch:del'   },
#   'show':          {'method': 'get',     'url': '/admin/role/$id'},
#   'add':           {'method': 'post',    'url': '/admin/role'},
#   'edit':          {'method': 'put',     'url': '/admin/role/$id'},
#   'del':           {'method': 'delete',  'url': '/admin/role/$id'},
#   'switch':        {'method': 'put',     'url': '/admin/role/status/$id'},
#   'bindPowerEdit': {'method': 'get',     'url': '/admin/role/power/$id'},
#   'bindPowerShow': {'method': 'get',     'url': '/admin/power'},
}


def getLogJson(val):
  permissions = val


  logJson = {
    "type": "page",
    # "title": "日志管理",
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
                  {
                    "label": "批量删除",
                    "actionType": "ajax",
                    "hidden": api["batchDel"]["permission"] not in permissions,
                    "api": {
                          "method": api["batchDel"]["method"],
                          "url": api["batchDel"]["url"]
                    },
                    "confirmText": "确定要批量删除?"
                  },
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
                  'bulkActions',
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
                    "align": "center",
                  },
                  {
                    "type": "text",
                    "name": "uid",
                    "label": "UID",
                    "align": "center",
                  },
                  {
                    "type": "text",
                    "name": "ip",
                    "label": "IP地址",
                    "align": "center",
                  },
                  {
                    "name": "method",
                    "label": "请求方式",
                    # "type": "text",
                    "align": "center",
                    "type": "mapping",
                    "map": {
                        "GET": "<span class=\"label label-info\">GET</span>",
                        "POST": "<span class=\"label label-success\">POST</span>",
                        "PUT": "<span class=\"label label-warning\">PUT</span>",
                        "DELETE": "<span class=\"label label-danger\">DELETE</span>",
                        "*": "其他：${type}"
                    }
                  },
                  
                  {
                    "type": "text",
                    "name": "url",
                    "label": "请求地址",
                    "align": "center",
                  },
                  {
                    "type": "html",
                    "name": "desc",
                    "label": "请求参数",
                    "align": "center",
                  },
                  {
                    "type": "status",
                    "name": "success",
                    "label": "请求结果",
                    "align": "center",
                    "map": {
                      True: "fa fa-check-circle",
                      False: "fa fa-times-circle"
                    },
                    "labelMap": {
                      True: "正常",
                      False: "异常"
                    },
                  },
                  {
                    "type": "text",
                    "name": "user_agent",
                    "label": "浏览器",
                    "align": "center",
                  },
                  {
                    "type": "date",
                    "name": "create_time",
                    "label": "创建时间",
                    "align": "center",
                    "format": "YYYY-MM-DD HH:mm:ss"
                  },
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


  return logJson