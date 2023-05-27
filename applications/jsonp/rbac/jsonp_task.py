# from flask import g

# g.permissions = ['admin:user:show','admin:user:add','admin:user:edit','admin:user:del']

# "hidden": "admin:user:deletea" not in permission
api = {
  'all':    {'method': 'get',     'url': '/admin/task/all'        , 'permission': 'admin:task:list' },
  'list':   {'method': 'get',     'url': '/admin/task/list'       , 'permission': 'admin:task:list' },
  'show':   {'method': 'get',     'url': '/admin/task/$id'        , 'permission': 'admin:task:show' },
  'add':    {'method': 'post',    'url': '/admin/task'            , 'permission': 'admin:task:add'  },
  'edit':   {'method': 'put',     'url': '/admin/task/$id'        , 'permission': 'admin:task:edit' },
  'run':    {'method': 'post',    'url': '/admin/task/run/$id'    , 'permission': 'admin:task:edit' },
  'switch': {'method': 'put',     'url': '/admin/task/status/$id' , 'permission': 'admin:task:edit' },
  'del':    {'method': 'delete',  'url': '/admin/task/$id'        , 'permission': 'admin:task:del'  },
}

def getTaskJson(val):
  permissions = val

  taskJson = {
    "type": "page",
    # "title": "计划任务管理",
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
                        "body": [
                          {
                                    "type": "radios",
                                    "name": "type",
                                    "label": "触发器",
                                    "required": True,
                                    "inline": True,
                                    "value": "date",
                                    "options": [
                                        {
                                            "label": "一次任务",
                                            "value": "date"
                                        },
                                        {
                                            "label": "间隔任务",
                                            "value": "interval"
                                        },
                                        {
                                            "label": "周期任务",
                                            "value": "cron"
                                        }
                                    ]
                                    
                          },

                          {
                            "name": "name",
                            "label": "任务名称",
                            "type": "input-text",
                            "required": True,
                          },
                          {
                                "label": "任务函数",
                                "type": "select",
                                "name": "functions",
                                "required": True,
                                "joinValues": False,
                                "extractValue": True,
                                "searchable": True,
                                "hidden": api['all']['permission'] not in permissions,
                                "source": {
                                  "method": api['all']['method'],
                                  "url": api['all']['url'],
                                    # "responseData": {
                                    #   "options": "${rows|pick:label~roleName,value~id}",
                                    # }
                                }
                          },
                          {
                            "type": "input-datetime",
                            "name": "datetime",
                            "label": "运行时间",
                            "format": "YYYY-MM-DD HH:mm:ss",
                            "hiddenOn": "data.type != \"date\"",
                            "clearValueOnHidden": True,
                            "required": True,
                          },
                          {
                            "type": "native-number",
                            "name": "seconds",
                            "label": "秒",
                            "align": "center",
                            "hiddenOn": "data.type != \"interval\"",
                            "clearValueOnHidden": True,
                            "required": True,
                            "placeholder": '必须大于0',
                            "validations": {
                                    'minimum': 1,
                            },
                            "validationErrors": {
                                    "minimum": "必须大于0",
                            },
                          },
                          
                          {
                            "type": "input-text",
                            "name": "day_of_week",
                            "label": "周几",
                            "align": "center",
                            "hiddenOn": "data.type != \"cron\"",
                            "clearValueOnHidden": True,
                            "placeholder": '例: 周一到周三: 1-3; 周一和周三: 1,3;',
                          },
                          {
                            "type": "native-number",
                            "name": "hour",
                            "label": "时",
                            "align": "center",
                            "hiddenOn": "data.type != \"cron\"",
                            "clearValueOnHidden": True,
                            "value": 00,
                          },
                          {
                            "type": "native-number",
                            "name": "minute",
                            "label": "分",
                            "align": "center",
                            "hiddenOn": "data.type != \"cron\"",
                            "clearValueOnHidden": True,
                            "value": 00,
                          },
                          {
                            "type": "native-number",
                            "name": "second",
                            "label": "秒",
                            "align": "center",
                            "hiddenOn": "data.type != \"cron\"",
                            "clearValueOnHidden": True,
                            "value": 00,
                          },
                          
                          # {
                          #   "type": "native-number",
                          #   "name": "month",
                          #   "label": "月",
                          #   "align": "center",
                          #   "hiddenOn": "data.type != \"interval\"",
                          #   "clearValueOnHidden": True,
                          #   "required": True,
                          #   "value": 0,
                          # },
                          # {
                          #   "type": "native-number",
                          #   "name": "weeks",
                          #   "label": "周",
                          #   "align": "center",
                          #   "hiddenOn": "data.type != \"interval\"",
                          #   "clearValueOnHidden": True,
                          #   "required": True,
                          #   "value": 0,
                          # },
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
                    "name": "name",
                    "label": "任务名称",
                    "type": "text",
                    "align": "center",
                    "copyable": True
                  },
                  {
                    "type": "text",
                    "name": "func",
                    "label": "任务函数",
                    "align": "center",
                  },
                  {
                    # "type": "text",
                    "name": "trigger",
                    "label": "任务触发器",
                    "align": "center",
                    "type": "mapping",
                    "map": {
                        "date": "<span class=\"label label-info\">一次任务</span>",
                        "interval": "<span class=\"label label-success\">间隔任务</span>",
                        "cron": "<span class=\"label label-warning\">周期任务</span>",
                        "*": "其他：${type}"
                    }
                  },
                  {
                    "type": "text",
                    "name": "second",
                    "label": "秒",
                    "align": "center",
                  },
                  {
                    "type": "text",
                    "name": "minute",
                    "label": "分",
                    "align": "center",
                  },
                  {
                    "type": "text",
                    "name": "hour",
                    "label": "时",
                    "align": "center",
                  },
                  {
                    "type": "text",
                    "name": "day_of_week",
                    "label": "周天",
                    "align": "center",
                  },
                  # {
                  #   "type": "text",
                  #   "name": "start_date",
                  #   "label": "任务开始时间",
                  #   "align": "center",
                  # },
                  {
                    "type": "switch",
                    "name": "enable",
                    "label": "任务状态",
                    "align": "center",
                    "falseValue": '0',
                    "trueValue":  '1',
                    "onText": "运行中",
                    "offText": "已停用",
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
                  # {
                  #   "type": "tpl",
                  #   "label": "是否运行",
                  #   "tpl": "${next_run_time == null ? '<span class=\"cxd-MappingField\"><span class=\"cxd-StatusField cxd-StatusField--warning\"><i class=\"cxd-Status-icon fa-regular fa-circle-pause\"></i><span class=\"cxd-StatusField-label\">已暂停</span></span></span>' : '<span class=\"cxd-StatusField cxd-StatusField--pending\"><i class=\"cxd-Status-icon rolling\"></i><span class=\"cxd-StatusField-label\">运行中</span></span>'}",
                  #   "align": "center",
                  # },
                  # {
                  #   "label": "状态",
                  #   "name": "next_run_time",
                  #   "align": "center",
                  #   "type": "mapping",
                  #   "map": {
                  #       "null": "pending",
                  #       "*": "其他：${type}"
                  #   }
                  # },
                  {
                    "type": "operation",
                    "label": "操作",
                    "align": "center",
                    "fixed": "right",
                    "buttons": [
                      {
                        "type": "action",
                        "label": "立即运行",
                        "actionType": "ajax", 
                        "hidden": api['run']['permission'] not in permissions,
                        "api": {
                          "method": api['run']['method'],
                          "url": api['run']['url']
                        }
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
                          "url": api['edit']['url']
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


  return taskJson