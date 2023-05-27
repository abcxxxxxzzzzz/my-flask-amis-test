# from flask import g

# g.permissions = ['admin:user:show','admin:user:add','admin:user:edit','admin:user:del']

# "hidden": "admin:user:deletea" not in permission
api = {
  'list':   {'method': 'get',     'url': '/admin/handicap/list'        , 'permission': 'admin:handicap:list'  },
  'show':   {'method': 'get',     'url': '/admin/handicap/$id'         , 'permission': 'admin:handicap:show'  },
  'add':    {'method': 'post',    'url': '/admin/handicap'             , 'permission': 'admin:handicap:add'   },
  'edit':   {'method': 'put',     'url': '/admin/handicap/$id'         , 'permission': 'admin:handicap:edit'  },
  'del':    {'method': 'delete',  'url': '/admin/handicap/$id'         , 'permission': 'admin:handicap:del'   },
}

def getHandicapJson(val):
  permissions = val

  handicapJson = {
    "type": "page",
    # "title": "盘口管理",
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
                            "type": "input-text",
                            "name": "name",
                            "label": "名称",
                            "required": True,
                            "validations": {
                              'maxLength': 50,
                            },
                            "validationErrors": {
                              "maxLength": "超出 $1 长度范围",
                            },
                          },
                        ]
                      }
                    },
                    "align": "left",
                  },
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
                    "name": "name",
                    "label": "盘口",
                    "type": "text",
                    "align": "center",
                    "copyable": True
                  },

                  {
                    "type": "date",
                    "name": "create_at",
                    "label": "创建时间",
                    "align": "center",
                    "format": "YYYY-MM-DD HH:mm:ss"
                  },
                  {
                    "type": "date",
                    "name": "update_at",
                    "label": "更新时间",
                    "align": "center",
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
                                "name": "name",
                                "label": "用户名",
                                "type": "input-text",
                                "validations": {
                                  'maxLength': 50,
                                },
                                "validationErrors": {
                                  "maxLength": "超出 $1 长度范围",
                                },
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


  return handicapJson