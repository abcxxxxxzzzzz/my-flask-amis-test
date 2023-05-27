from flask import g

# g.permissions = ['admin:user:show','admin:user:add','admin:user:edit','admin:user:del']

# "hidden": "admin:user:deletea" not in permission
api = {
  'list':   {'method': 'get',     'url': '/admin/domain/https/list'        , 'permission': 'admin:domain:https:list'  },
  'show':   {'method': 'get',     'url': '/admin/domain/https/$id'         , 'permission': 'admin:domain:https:show'  },
  'add':    {'method': 'post',    'url': '/admin/domain/https'             , 'permission': 'admin:domain:https:add'   },
  'edit':   {'method': 'put',     'url': '/admin/domain/https/$id'         , 'permission': 'admin:domain:https:edit'  },
  'switch': {'method': 'put',     'url': '/admin/domain/https/status/$id'  , 'permission': 'admin:domain:https:edit'  },
  'del':    {'method': 'delete',  'url': '/admin/domain/https/$id'         , 'permission': 'admin:domain:https:del'   },
  'batchDel':    {'method': 'delete',  'url': '/admin/domain/https/batch'         , 'permission': 'admin:domain:https:batch:del'   },
  'batchAdd':    {'method': 'post',  'url': '/admin/domain/https/batch'         , 'permission': 'admin:domain:https:batch:add'   },

  'handicap':  {'method': 'get',     'url': '/admin/handicap/list'      , 'permission': 'admin:handicap:list'   },  # 获取部门
}

def getJson(val):
  permissions = val

  Json = {
    "type": "page",
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
                    "level": "danger",
                    "size": "sm",
                    "hidden": api["batchDel"]["permission"] not in permissions,
                    "api": {
                          "method": api["batchDel"]["method"],
                          "url": api["batchDel"]["url"],
                          "data": {
                            "ids": "${ids|raw}"
                          }
                    },
                    "confirmText": "确定要批量删除?"
                  },
                ],
                "itemActions": [
                ],
                "features": [
                  "create",
                  "update",
                  "delete",
                  "filter"
                ],
                "filterColumnCount": 3,
                "headerToolbar": [
                  {
                    "label": "新增",
                    "type": "button",
                    "icon": "fa fa-plus",
                    "actionType": "dialog",
                    "level": "primary",
                    "size": "sm",
                    "hidden": api['add']['permission'] not in permissions,
                    "dialog": {
                      "title": "新增",
                      "body": {
                        "type": "form",
                        "api": {
                          "method": api['add']['method'],
                          "url": api['add']['url']
                        },
                        "body": [
                          {
                            "type": "select",
                            "name": "handicapId",
                            "label": "部门",
                            "align": "center",
                            "value": "${handicap|pick:id}",
                            "searchable": True,
                            "clearable": True,
                            "required": True,
                            "source": {
                              "method": api['handicap']['method'],
                              "url": api['handicap']['url'],
                              "responseData": {
                                "options": "${rows|pick:label~name,value~id}"
                              }
                            },
                          },
                          {
                            "type": "input-text",
                            "name": 'name',
                            "label": "域名",
                            "align": "center",
                            "placeholder": "请输入名称",
                          }
                        ]
                      }
                    },
                    "align": "left",
                  },
                  {
                    "label": "批量添加",
                    "type": "button",
                    "icon": "fa-solid fa-seedling",
                    "actionType": "dialog",
                    "level": "success",
                    "size": "sm",
                    "hidden": api['batchAdd']['permission'] not in permissions,
                    "dialog": {
                      "title": "批量添加",
                      "closeOnEsc": True,
                      "closeOnOutside": True,
                      "body": {
                        "type": "form",
                        "resetAfterSubmit": True,
                        "api": {
                              "method": api["batchAdd"]["method"],
                              "url": api["batchAdd"]["url"]
                        },
                        "body": [
                            {
                              "type": "select",
                              "name": "handicapId",
                              "label": "部门",
                              "align": "center",
                              "value": "${handicap|pick:id}",
                              "searchable": True,
                              "clearable": True,
                              "required": True,
                              "source": {
                                "method": api['handicap']['method'],
                                "url": api['handicap']['url'],
                                "responseData": {
                                  "options": "${rows|pick:label~name,value~id}"
                                }
                              },
                            },
                            {
                              "name": "batchadd",
                              "type": "textarea",
                              "clearable": True,
                              "showCounter": True,
                              "required": True,
                              "minRows": 10,
                              "placeholder": "批量添加数据, 一行一个" ,
                              # "label": "批量查询"
                            },
                        ],
                        
                      }
                    },
                    "align": "left",
                  },

                  "bulkActions",
                  {
                    "type": "columns-toggler",
                    "align": "right",
                    "size": "sm",
                  },
                  {
                    "type": "export-excel",
                    "tpl": "内容",
                    "id": "u:adc705a92fe1",
                    "align": "right",
                    "size": "sm",
                  },
                  {
                    "type": "reload",
                    "align": "right",
                    "icon": "fa-solid fa-arrows-rotate",
                    "label": "刷新",
                    "tooltip": "",
                    "level": "default",
                    "size": "sm",
                  },
                  {
                          "type": "search-box",
                          "align": "right",
                          "name": "search",
                          "placeholder": "请输入名称",
                          "mini": True,
                          "addOn": {
                                  "label": "搜索",
                                  "type": "submit"
                          }
                  },
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
                "columns": [
                  {
                    "name": "id",
                    "label": "ID",
                    "type": "text",
                    "align": "center"
                  },
                  {
                    "name": "handicap",
                    "label": "部门",
                    "type": "tpl",
                    "tpl": "${handicap.name}",
                    "align": "center",
                  },
                  {
                    "name": "name",
                    "label": "域名名称",
                    "type": "text",
                    "align": "center",
                    "copyable": True
                  },
                  {
                    "name": "expir_day",
                    "label": "证书剩余时间",
                    "type": "text",
                    "align": "center",
                    "sortable": True
                  },
                  {
                    "type": "switch",
                    "label": "启用",
                    "name": "enable",
                    "falseValue": '0',
                    "trueValue": '1',
                    "align": "center",
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
                                  "method": api['switch']['method'],
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
                    "name": "remark",
                    "label": "备注",
                    "type": "text",
                    "align": "center",
                  },
                  {
                    "type": "date",
                    "name": "create_at",
                    "label": "创建时间",
                    "align": "center",
                    "format": "YYYY-MM-DD HH:mm:ss",
                    # "sortable": True
                  },
                  {
                    "type": "date",
                    "name": "update_at",
                    "label": "更新时间",
                    "align": "center",
                    "format": "YYYY-MM-DD HH:mm:ss",
                    # "sortable": True
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
                        "hidden": api['edit']['permission'] not in permissions,
                        "dialog": {
                          "title": "编辑",
                          "body": {
                            "type": "form",
                            "api": {
                              "method": api['edit']['method'],
                              "url": api['edit']['url'],
                            },
                            "body": [
                              {
                                "type": "select",
                                "name": "handicapId",
                                "label": "部门",
                                "align": "center",
                                "required": True,
                                # "disabled": True,
                                # "size": "full",
                                # "multiple": True,
                                # "joinValues": False,
                                # "extractValue": True,
                                "value": "${handicap|pick:id}",
                                "searchable": True,
                                "clearable": True,
                                "source": {
                                  "method": api['handicap']['method'],
                                  "url": api['handicap']['url'],
                                  "responseData": {
                                    "options": "${rows|pick:label~name,value~id}"
                                  }
                                },
                              },
                              {
                                "name": "name",
                                "label": "域名名称",
                                "type": "input-text",
                                "required": True,
                              },
                              {
                                "name": "remark",
                                "label": "备注",
                                "type": "input-text",
                              },
                            ]
                          }
                        },
                        "id": "u:6e01ac9132f2"
                      },
                      {
                        "type": "button",
                        "label": "删除",
                        "actionType": "ajax",
                        "level": "link",
                        "className": "text-danger",
                        "confirmText": "确定要删除 $username ？",
                        "hidden": api['del']['permission'] not in permissions,
                        "api": {
                          "method": api['del']['method'],
                          "url": api['del']['url']
                        },
                        "id": "u:3c44ea51974a"
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
            "id": "u:fdf20294c8bd"
          }
        ],
        "style": {
          "position": "static"
        },
        "direction": "row",
        "justify": "flex-start",
        "alignItems": "stretch",
        "id": "u:358b8cdb82f8"
      }
    ],
  }


  return Json