from flask import g

# g.permissions = ['admin:user:show','admin:user:add','admin:user:edit','admin:user:del']

# "hidden": "admin:user:deletea" not in permission
api = {
  'list':      {'method': 'get',     'url': '/admin/user/list'        , 'permission': 'admin:user:list'  },
  'show':      {'method': 'get',     'url': '/admin/user/$id'         , 'permission': 'admin:user:show'  },
  'add':       {'method': 'post',    'url': '/admin/user'             , 'permission': 'admin:user:add'   },
  'edit':      {'method': 'put',     'url': '/admin/user/$id'         , 'permission': 'admin:user:edit'  },
  'switch':    {'method': 'put',     'url': '/admin/user/status/$id'  , 'permission': 'admin:user:edit'  },
  'del':       {'method': 'delete',  'url': '/admin/user/$id'         , 'permission': 'admin:user:del'   },
  'role':      {'method': 'get',     'url': '/admin/role/list'        , 'permission': 'admin:role:list'  },       # 获取角色 
  'handicap':  {'method': 'get',     'url': '/admin/handicap/list'    , 'permission': 'admin:handicap:list'   },  # 获取部门
}

def getUserJson(val):
  permissions = val

  userJson = {
    "type": "page",
    # "title": "用户管理",
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
                    "hidden": api['add']['permission'] not in permissions,
                    "dialog": {
                      "title": "新增",
                      "body": {
                        "type": "form",
                        "api": {
                          "method": api['add']['method'],
                          "url": api['add']['url']
                        },
                        "rules": [
                                {
                                        "rule": "data.password == data.password2",
                                        "message": "两次密码不一致",
                                        "name": [
                                                "password",
                                                "password2"
                                        ]
                                }
                        ],
                        "body": [
                          {
                            "type": "input-text",
                            "name": "username",
                            "label": "用户名",
                            "required": True,
                          },
                          {
                            "type": "input-text",
                            "name": "realname",
                            "label": "名称",
                            "required": True,
                          },
                          {
                            "type": "input-password",
                            "name": "password",
                            "label": "密码",
                            "required": True,
                            "validations": {
                                    'minLength': 6,
                                    'maxLength': 50,
                            },
                            "validationErrors": {
                                    "minLength": "最少输入$1以上的数字哈",
                                    "maxLength": "最多输入$1以上的数字哈",
                            },
                          },
                          {
                            "type": "input-password",
                            "name": "password2",
                            "label": "重复密码",
                            "required": True,
                            "validations": {
                                    'minLength': 6,
                                    'maxLength': 50,
                            },
                            "validationErrors": {
                                    "minLength": "最少输入$1以上的数字哈",
                                    "maxLength": "最多输入$1以上的数字哈",
                            },
                          },
                          {
                            "type": "switch",
                            "label": "启用",
                            "name": "enable",
                            "falseValue": '0',
                            "trueValue": '1',
                            "onText": "已启用",
                            "offText": "已禁用"
                          },
                          {
                            "label": "角色选择",
                            "type": "select",
                            "name": "roleIds",
                            # "size": "sm",
                            "multiple": True,
                            "joinValues": False,
                            "extractValue": True,
                            "searchable": True,
                            "source": {
                              "method": api['role']['method'],
                              "url": api['role']['url'],
                              "responseData": {
                                "options": "${rows|pick:label~roleName,value~id}"
                              }
                            },
                          },
                          {
                              "type": "select",
                              "name": "handicapId",
                              "label": "部门",
                              "align": "center",
                              # "required": True,
                              # "size": "full",
                              # "multiple": True,
                              # "joinValues": False,
                              # "extractValue": True,
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
                    "align": "center"
                  },
                  {
                    "name": "username",
                    "label": "用户名",
                    "type": "text",
                    "align": "center",
                    "copyable": True
                  },
                  {
                    "type": "text",
                    "name": "realname",
                    "label": "名称",
                    "align": "center"
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
                    "name": "role",
                    "label": "角色",
                    "type": "each",
                    "align": "center",
                    "placeholder": "-",
                    "items": {
                      "type": "tpl",
                      "tpl": "<span class='label label-success m-l-sm'><%= data.roleName %></span>"
                    }
                  },
                  {
                    "type": "mapping",
                    "name": "is_super",
                    "label": "是否超级管理员",
                    "map": {
                        # "*": "<span class=\"label label-info\">否</span>",
                        "1": "<span class=\"label label-success\">是</span>",
                        "*": "<span class=\"label label-info\">否</span>",
                        # "*": "其他：${type}"
                    }
                  },
                  {
                    "type": "tpl",
                    "tpl": "${handicap.name}",
                    "label": "部门",
                    "align": "center"
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
                    "label": "修改时间",
                    "format": "YYYY-MM-DD HH:mm:ss",
                    "align": "center"
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
                                "name": "username",
                                "label": "用户名",
                                "type": "input-text"
                              },
                              {
                                "name": "realname",
                                "label": "名称",
                                "type": "input-text"
                              },
                              # {
                              #   "type": "switch",
                              #   "label": "启用",
                              #   "name": "enable",
                              #   "falseValue": False,
                              #   "trueValue": True,
                              # },
                              {
                                "label": "角色选择",
                                "type": "select",
                                "name": "roleIds",
                                "multiple": True,
                                "joinValues": False,
                                "extractValue": True,
                                "searchable": True,
                                "value": "${role|pick:id}",
                                "source": {
                                "method": api['role']['method'],
                                "url": api['role']['url'],
                                  "responseData": {
                                    "options": "${rows|pick:label~roleName,value~id}",
                                  }
                                }
                              },
                              {
                                "type": "select",
                                "name": "handicapId",
                                "label": "部门",
                                "align": "center",
                                # "required": True,
                                # "size": "full",
                                # "multiple": True,
                                # "joinValues": False,
                                # "extractValue": True,
                                "searchable": True,
                                "clearable": True,
                                "value": "${handicap.id}",
                                "source": {
                                  "method": api['handicap']['method'],
                                  "url": api['handicap']['url'],
                                  "responseData": {
                                    "options": "${rows|pick:label~name,value~id}"
                                  }
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


  return userJson