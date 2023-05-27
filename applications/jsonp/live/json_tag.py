from flask import g

# g.permissions = ['admin:user:show','admin:user:add','admin:user:edit','admin:user:del']

# "hidden": "admin:user:deletea" not in permission
api = {
  'list':   {'method': 'get',     'url': '/admin/tag/list'        , 'permission': 'admin:tag:list'  },
  'show':   {'method': 'get',     'url': '/admin/tag/$id'         , 'permission': 'admin:tag:show'  },
  'add':    {'method': 'post',    'url': '/admin/tag'             , 'permission': 'admin:tag:add'   },
  'edit':   {'method': 'put',     'url': '/admin/tag/$id'         , 'permission': 'admin:tag:edit'  },
  'del':    {'method': 'delete',  'url': '/admin/tag/$id'         , 'permission': 'admin:tag:del'   },

  'handicap':  {'method': 'get',     'url': '/admin/handicap/list'      , 'permission': 'admin:handicap:list'   },  # 获取部门
}

def getJson(val):
  permissions = val

  Json = {
    "type": "page",
    # "title": "部门管理",
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
                            "hidden": g.user.is_super != 1,
                            "type": "select",
                            "name": "handicapId",
                            "label": "部门",
                            "align": "center",
                            # "required": True,
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
                          {
                              "label": "标签颜色",
                              "type": "select",
                              "name": "color",
                              "required": True,
                              # "menuTpl": "<div>${label} 值：${value}, 当前是否选中: ${checked}</div>",
                              "menuTpl": "<div><span class=\"cxd-Tag cxd-Tag--normal cxd-Tag--normal--${value} cxd-Tag--normal--hasColor\"><span class=\"cxd-Tag-text\">${label}</span></span></div>",
                              "options": [
                                  {
                                    "label": "深蓝",
                                    "value": "active"
                                  },
                                  {
                                    "label": "浅灰",
                                    "value": "inactive"
                                  },
                                  {
                                    "label": "深红",
                                    "value": "error"
                                  },
                                  {
                                    "label": "深绿",
                                    "value": "success"
                                  },
                                  {
                                    "label": "浅蓝",
                                    "value": "processing"
                                  },
                                  {
                                    "label": "浅橙",
                                    "value": "warning"
                                  }
                              ]
                          }
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
                    "hidden": g.user.is_super != 1,
                    "name": "handicap",
                    "label": "部门",
                    "type": "tpl",
                    "tpl": "${handicap.name}",
                    "align": "center",
                    "copyable": True,
                  },
                  {
                    "name": "name",
                    "label": "标签名称",
                    "type": "text",
                    "align": "center",
                    "copyable": True
                  },
                  {
                    # "type": "text",
                    "name": "color",
                    "label": "标签颜色",
                    "align": "center",
                    "type": "mapping",
                    "map": {
                        "active": "<span class=\"cxd-Tag cxd-Tag--normal cxd-Tag--normal--active cxd-Tag--normal--hasColor\"><span class=\"cxd-Tag-text\">深蓝</span></span>",
                        "inactive": "<span class=\"cxd-Tag cxd-Tag--normal cxd-Tag--normal--inactive cxd-Tag--normal--hasColor\"><span class=\"cxd-Tag-text\">浅灰</span></span>",
                        "error": "<span class=\"cxd-Tag cxd-Tag--normal cxd-Tag--normal--error cxd-Tag--normal--hasColor\"><span class=\"cxd-Tag-text\">深红</span></span>",
                        "success": "<span class=\"cxd-Tag cxd-Tag--normal cxd-Tag--normal--success cxd-Tag--normal--hasColor\"><span class=\"cxd-Tag-text\">深绿</span></span>",
                        "processing": "<span class=\"cxd-Tag cxd-Tag--normal cxd-Tag--normal--processing cxd-Tag--normal--hasColor\"><span class=\"cxd-Tag-text\">浅蓝</span></span>",
                        "warning": "<span class=\"cxd-Tag cxd-Tag--normal cxd-Tag--normal--warning cxd-Tag--normal--hasColor\"><span class=\"cxd-Tag-text\">浅橙</span></span>",
                        "*": "其他：${type}"
                    }
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
                                "hidden": g.user.is_super != 1,
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
                                "label": "名称",
                                "type": "input-text",
                                "required": True,
                              },
                              {
                                "label": "标签颜色",
                                "type": "select",
                                "name": "color",
                                # "menuTpl": "<div>${label} 值：${value}, 当前是否选中: ${checked}</div>",
                                "menuTpl": "<div><span class=\"cxd-Tag cxd-Tag--normal cxd-Tag--normal--${value} cxd-Tag--normal--hasColor\"><span class=\"cxd-Tag-text\">${label}</span></span></div>",
                                "options": [
                                    {
                                      "label": "深蓝",
                                      "value": "active"
                                    },
                                    {
                                      "label": "浅灰",
                                      "value": "inactive"
                                    },
                                    {
                                      "label": "深红",
                                      "value": "error"
                                    },
                                    {
                                      "label": "深绿",
                                      "value": "success"
                                    },
                                    {
                                      "label": "浅蓝",
                                      "value": "processing"
                                    },
                                    {
                                      "label": "浅橙",
                                      "value": "warning"
                                    }
                                ]
                              }
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