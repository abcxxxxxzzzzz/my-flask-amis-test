from flask import g

# g.permissions = ['admin:user:show','admin:user:add','admin:user:edit','admin:user:del']

# "hidden": "admin:user:deletea" not in permission
api = {
  "batchAdd":  {"method": "post",    "url": "/admin/title/batch"     ,  'permission': 'admin:title:batch:add'   },
  "batchEdit": {"method": "put",     "url": "/admin/title/batch"     ,  'permission': 'admin:title:batch:edit'   },
  'download':  {'method': 'get',     'url': '/admin/title'           ,  'permission': 'admin:title:batch:add'  }, # 模板
  'exportAll': {'method': 'get',     'url': '/admin/title/all'       ,  'permission': 'admin:title:batch:list'  }, # 模板
  "batchDel":  {"method": "delete",  "url": "/admin/title/batch"     ,  'permission': 'admin:title:batch:del'   },
  "truncateTable":  {"method": "delete",  "url": "/admin/title/truncate",  'permission': 'admin:title:batch:truncate'   }, # 清空表
  'list':      {'method': 'get',     'url': '/admin/title/list'      ,  'permission': 'admin:title:list'   },
  'show':      {'method': 'get',     'url': '/admin/title/$id'       ,  'permission': 'admin:title:show'   },
  'add':       {'method': 'post',    'url': '/admin/title'           ,  'permission': 'admin:title:add'   },
  'edit':      {'method': 'put',     'url': '/admin/title/$id'       ,  'permission': 'admin:title:edit'   },
  'del':       {'method': 'delete',  'url': '/admin/title/$id'       ,  'permission': 'admin:title:del'   },


  'weight':    {'method': 'get',  'url': '/admin/title/weight'       ,  'permission': 'admin:title:list'   },
  'tag':    {'method': 'get',  'url': '/admin/title/tag'       ,  'permission': 'admin:title:list'   },
  'upload_tag':    {'method': 'get',  'url': '/admin/title/upload_tag'       ,  'permission': 'admin:title:list'   },

  
}     

def getTitleJson(val):
  permissions = val

  titleJson = {
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
                "title": "查询条件",
                "type": "form",
                "target": "my_crud",
                "hidden": True,
                "id": "search-more",
                "body": [
                  {
                    "type":'group',
                    "body": [
                          {
                            "label": "域名权重",
                            "type": "select",
                            "name": "weight",
                            "size": "full",
                            "mode": "horizontal",
                            "multiple": True,
                            "clearable": True,
                            # "joinValues": False,
                            # "extractValue": True,
                            # "searchable": True,
                            # "clearable": True,
                            # "hidden": api['weight']['permission'] not in permissions,
                            "source": {
                              "method": api['weight']['method'],
                              "url": api['weight']['url'],
                              "responseData": {
                                "options": "${rows|pick:label~label,value~weight}"
                              }
                            },
                          },

                          {
                            "label": "爬虫标签",
                            "type": "select",
                            "name": "tag",
                            "size": "full",
                            "mode": "horizontal",
                            "clearable": True,
                            # "multiple": True,
                            # "joinValues": False,
                            # "extractValue": True,
                            # "searchable": True,
                            # "clearable": True,
                            # "hidden": api['weight']['permission'] not in permissions,
                            "source": {
                              "method": api['tag']['method'],
                              "url": api['tag']['url'],
                              "responseData": {
                                "options": "${rows|pick:label~label,value~tag}"
                              }
                            },
                          },
                          {
                            "label": "上传标签",
                            "type": "select",
                            "name": "upload_tag",
                            "size": "full",
                            "mode": "horizontal",
                            "clearable": True,
                            "multiple": True,
                            # "joinValues": False,
                            # "extractValue": True,
                            # "searchable": True,
                            # "clearable": True,
                            # "hidden": api['weight']['permission'] not in permissions,
                            "source": {
                              "method": api['upload_tag']['method'],
                              "url": api['upload_tag']['url'],
                              "responseData": {
                                "options": "${rows|pick:label~label,value~upload_tag}"
                              }
                            },
                          },
                          {
                            "label": "状态",
                            "type": "select",
                            "name": "status",
                            "size": "full",
                            "mode": "horizontal",
                            "searchable": True,
                            "clearable": True,
                            "options": [
                                        {
                                            "label": "未查询",
                                            "value": "0"
                                        },
                                        {
                                            "label": "已查询",
                                            "value": "1"
                                        },
                                        {
                                            "label": "站长待查询",
                                            "value": "2"
                                        },
                                        {
                                            "label": "域名待查询",
                                            "value": "3"
                                        },
                                        {
                                            "label": "待站长二次查询",
                                            "value": "4"
                                        },
                                  ]
                            },
                          {
                            "type": "input-text",
                            "name": "more",
                            "label": "模糊搜索",
                            "clearable": True,
                            "placeholder": "搜索描述：多个逗号分隔",
                            # "size": "md",
                            "size": "full",
                            "mode": "horizontal",
                            "labelClassName": "p-sm"
                          },
                    ],

                    # "submitText": "搜索",
                  },
                  {
                            "type": "input-datetime-range",
                            "name": "daytime",
                            "timeFormat": "HH:mm:ss",
                            "label": "日期时间范围",
                            "size": "full",
                            "mode": "horizontal",
                            "clearable": True,
                            "format": "YYYY-MM-DD HH:mm:ss"
                  },
                ],
                
                "actions": [
                      # {
                      #   "type": "reset",
                      #   "label": "重置",
                      #   "size": "sm",
                      # },
                      {
                        "type": "button",
                        "label": "清空",
                        # "actionType": "clear-and-submit",
                        "size": "sm",
                        "onClick": "props.formStore.setValues({ids: '', tag: '','more':'','daytime':'','upload_tag': ''});"
                      },
                      {
                        "type": "submit",
                        "level": "primary",
                        "label": "查询",
                        "size": "sm",
                      },
                      {
                        "type": "button",
                        "level": "default",
                        "label": "隐藏",
                        "size": "sm",
                        "onEvent": {
                          "click": {
                            "actions": [
                              {
                                "actionType": "hidden",
                                "componentId": "search-more"
                              }
                            ]
                          }
                        }
                      },
                      {
                        "type": "button",
                        # "actionType": "ajax",
                        # "fileName": "下载的文件名",
                        "align": "right",
                        "size": "sm",
                        "label": "条件导出(默认全部)",
                        "icon": "fa-solid fa-download",
                        # "onClick": "alert('点击了按钮'); console.log(props.data);"
                        "onClick": """
                            props.onAction(event, 
                              {
                                actionType: "ajax",
                                api: {
                                  responseType: "blob",
                                  method: "%s",
                                  url: "%s",
                                  data: {
                                    tag: props.data.tag,
                                    title: props.data.title,
                                    status: props.data.status,
                                    more: props.data.more,
                                    daytime: props.data.daytime,
                                    upload_tag: props.data.upload_tag,
                                  }
                                }
                              }
                            )
                        """ % (api['exportAll']['method'],api['exportAll']['url'])
                      #   "api": {
                      #         "responseType": "blob",
                      #         "trackExpression": "${tag}",
                      #         "method": api['exportAll']['method'],
                      #         "url": api['exportAll']['url'] + "?/${tag}&${status}&$status&$tag"
                      #       },
                      #  'data': {
                      #    'test':  "${event.data}",
                      #    'test2': "${props.data}",
                      #    'test3': "${tag}",
                      #    'test4': "${status}",
                      #    'test5': "$status",
                      #    'test6': "${status}",
                      #    'test7': "${data}",
                      #    'test8': "$data",
                      #  }
                      },
                    ]

              },
              {
                "type": "crud",
                "name": "my_crud",
                "syncLocation": False,
                "api": {
                  "method": api['list']['method'],
                  "url": api['list']['url']
                },
                "bulkActions": [
                  {
                    "label": "恢复未查询",
                    "actionType": "ajax",
                    # "level": "default",
                    "size": "sm",
                    "hidden": api["batchEdit"]["permission"] not in permissions,
                    "api": {
                          "method": api["batchEdit"]["method"],
                          "url": api["batchEdit"]["url"],
                          "data": {
                            'ids': "$ids"
                          }
                    },
                    "confirmText": "确定要批量执行查询?"
                  },
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
                            'ids': "$ids"
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
                      # "actions": [],
                      "body": {
                        "type": "form",
                        "api": {
                          "method": api['add']['method'],
                          "url": api['add']['url']
                        },
                        "body": [
                          {
                            "type": "input-text",
                            "name": "url",
                            "label": "网址域名",
                            "required": True,
                          },
                        ]
                      }
                    },
                    
                    "align": "left",
                  },
                  {
                    "label": "上传",
                    "type": "button",
                    "icon": "fa-solid fa-arrow-up-from-bracket",
                    "actionType": "dialog",
                    "level": "enhance",
                    "size": "sm",
                    "hidden": api['batchAdd']['permission'] not in permissions,
                    "dialog": {
                      "title": "上传",
                      "closeOnEsc": True,
                      "closeOnOutside": True,
                      "body": {
                        "type": "form",
                        "api": {
                          "method": api['batchAdd']['method'],
                          "url": api['batchAdd']['url']
                        },
                        "body": [
                            {
                              "type": "input-excel",
                              "name": "excel",
                              "label": "上传 Excel",
                              # "required": True,
                            },
                            {
                              "type": "input-text",
                              "name": "uploadTag",
                              "label": "上传标签",
                              "placeholder": "请输入上传标签,默认是当前日期",
                              # "required": True,
                            },
                            {
                                "type": "tpl",
                                "tpl": "表头格式: <p style=\"color: green\">网址域名(必须) 权重(必须)</p>"
                            },
                            {
                                "type": "tpl",
                                "tpl": "<p style=\"color: red\">提示: 不限制上传次数，但必须是 .xlsx 结尾文件，支持添加已经存在网址域名</p>"
                            },
                            {
                              "label": "下载模板",
                              "type": "action",
                              "actionType": "download",
                              "hidden": api['download']['permission'] not in permissions,
                              "api": {
                                'method': api['download']['method'],
                                'url': api['download']['url'] + "/templatesUrl.xlsx",
                              }
                            },
                        ]
                      }
                    },
                    "align": "left",
                  },
                  {
                    "label": "批量搜索",
                    "type": "button",
                    "icon": "fa-solid fa-seedling",
                    "actionType": "dialog",
                    "level": "success",
                    "size": "sm",
                    # "hidden": api['upload']['permission'] not in permissions,
                    "dialog": {
                      "title": "批量搜索",
                      "closeOnEsc": True,
                      "closeOnOutside": True,
                      "actions": [
                            {
                              "type": "button",
                              "label": "清空",
                              "actionType": "clear",
                              "size": "sm",
                              # "onClick": "props.formStore.setValues({batchsearch: ''});"
                            },
                            {
                              "type": "submit",
                              # "actionType": "clear-and-submit",
                              "level": "primary",
                              "label": "批量搜索",
                              "size": "sm",
                            },
                        ],
                      "body": {
                        "type": "form",
                        "target": "my_crud",
                        "resetAfterSubmit": True,
                        "body": [
                            {
                              "name": "batchsearch",
                              "type": "textarea",
                              "clearable": True,
                              "showCounter": True,
                              "minRows": 10,
                              "placeholder": "批量精准搜索, 一行一个" ,
                              # "label": "批量查询"
                            },
                            {
                              "type": "tpl",
                              "tpl": "<p style='color: red'>提示: <span>批量查询之后,手动刷新或者重新打开 `批量查询` 清空查询数据，整个页面恢复原先所有数据</span></p>"
                            },
                            
                        ],
                        
                      }
                    },
                    "align": "left",
                  },
                  
                  {
                        "type": "button",
                        "label": "清空表",
                        "actionType": "ajax",
                        "level": "danger",
                        "icon": "fa-regular fa-trash-can",
                        "className": "text-danger",
                        "confirmText": "确定要清空当前页面所有数据么, 此操作不可挽回？",
                        "hidden": api['truncateTable']['permission'] not in permissions,
                        "api": {
                          "method": api['truncateTable']['method'],
                          "url": api['truncateTable']['url']
                        },
                  },

                  "bulkActions",
                  {
                    "type": "columns-toggler",
                    "align": "right"
                  },
                  {
                    "type": "export-excel",
                    "tpl": "内容",
                    "align": "right",
                    "size": "sm",
                    "icon": "fa-solid fa-download",
                    "label": "导出当页",
                  },
                  # {
                  #     "type": "export-csv",
                  #     # "target": "my_crud",
                  #     "align": "right",
                  #     "size": "sm",
                  #     "label": "条件导出",
                  #     "icon": "fa-solid fa-download",
                  #     "api": {
                  #           "method": api['exportAll']['method'],
                  #           "url": api['exportAll']['url'] + "?$tag&title"
                  #         },
                  #     # 'data': {
                  #     #   'test':  "${event.data}",
                  #     #   'test2': "${props.data}",
                  #     #   'test3': "${data}",
                  #     #   'test4': "${args}",
                  #     # }
                  # },
                  # {
                  #   # "target": "my_crud",
                  #   "type": "export-excel",
                  #   "align": "right",
                  #   "size": "sm",
                  #   "label": "导出(默认当页)",
                  #   "icon": "fa-solid fa-download",
                  # },
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
                    "type": "button",
                    "align": "right",
                    "icon": "fa-solid fa-magnifying-glass",
                    "level": "default",
                    "tooltip": "更多条件查询",
                    "size": "sm",
                    "onEvent": {
                      "click": {
                        "actions": [
                          {
                            "actionType": "show",
                            "componentId": "search-more"
                          }
                        ]
                      }
                    }
                  },
                  {
                          "type": "search-box",
                          "align": "right",
                          "name": "search",
                          "placeholder": "请输入网址域名",
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
                  500,
                  1000,
                  # 2000,
                  # 5000,
                  # 10000,
                ],
                "messages": {
                },
                "mode": "table",
                "columns": [
                        # {
                        #     "name": "id",
                        #     "label": "ID",
                        #     "type": "text",
                        #     "align": "center"
                        # },
                        {
                            "type": "text",
                            "name": "url",
                            "label": "网址域名",
                            "align": "center",
                            # "blank": True,
                            "copyable": True,
                            "toggled": True,
                            "fixed": "left"
                        },
                        {
                            "type": "text",
                            "name": "weight",
                            "label": "权重",
                            "align": "center",
                            # "blank": True,
                            # "copyable": True
                        },
                        
                        {
                          "type": "tpl",
                          "label": "网址标题",
                          "tpl": "${title|truncate:100}",
                          "width": '10%',
                        },
                        {
                          "type": "tpl",
                          "label": "网址关键词",
                          "tpl": "${keywords|truncate:100}",
                          "width": '30%',
                        },
                        {
                          "type": "tpl",
                          "label": "网址描述",
                          "tpl": "${description|truncate:100}",
                          "width": '20%',
                        },
                        # {
                        #     "type": "text",
                        #     "name": "title",
                        #     "label": "网址标题",
                        #     "align": "center",
                        #     "width": "10%",
                        #     "copyable": True
                        # },
                        # {
                        #     "type": "text",
                        #     "name": "keywords",
                        #     "label": "网址关键词",
                        #     "align": "center",
                        #     "width": "20%",
                        #     "copyable": True
                        # },
                        # {
                        #     "type": "text",
                        #     "name": "description",
                        #     "label": "网址描述",
                        #     "align": "center",
                        #     "width": "20%",
                        #     "copyable": True
                        # },
                        
                        {
                          "label": "标签",
                          "name": "tag",
                          "type": "mapping",
                          "align": "center",
                          # "value": "2",
                          "map": {
                            # "无标题": "<span class='label label-info'>获取站长数据成功</span>",
                            "获取站长数据成功": "<span class='label label-success'>获取站长数据成功</span>",
                            "获取域名页面数据成功": "<span class='label label-success'>获取域名页面数据成功</span>",
                            "获取站长数据失败": "<span class='label label-danger'>获取站长数据失败</span>",
                            "准备抓取站长数据": "<span class='label label-warning'>准备抓取站长数据</span>",
                            "准备抓取域名页面": "<span class='label label-info'>准备抓取域名页面</span>",
                            "待站长二次查询": "<span class='label label-warning'>待站长二次查询</span>",
                            # "无法访问": "<span class='label label-warning'>无法访问</span>",
                            "*": "<span class='label label-default'>未知${type}</span>"
                          },
                        },
                        {
                          "name": "status",
                          "label": "查询状态",
                          "type": "mapping",
                          "map": {
                              "0": "<span class=\"label label-warning\">未查询</span>",
                              "1": "<span class=\"label label-success\">已查询</span>",
                              "2": "<span class=\"label label-info\">站长待查询</span>",
                              "3": "<span class=\"label label-info\">域名待查询</span>",
                              "4": "<span class=\"label label-info\">待站长二次查询</span>",
                              "*": "未知：${type}"
                          }
                        },
                        {
                            "type": "date",
                            "name": "create_time",
                            "label": "创建时间",
                            "align": "center",
                            "format": "YYYY-MM-DD HH:mm:ss"
                        },
                        {
                            "type": "date",
                            "name": "update_time",
                            "label": "更新时间",
                            "align": "center",
                            "format": "YYYY-MM-DD HH:mm:ss"
                        },
                        {
                            "type": "operation",
                            "label": "操作",
                            # "align": "center",
                            "fixed": "right",
                            "buttons": [
                                {
                                    "label": "执行查询",
                                    "type": "button",
                                    "actionType": "ajax",
                                    "level": "link",
                                    "hidden": api['edit']['permission']  not in permissions,
                                    "api": {
                                      "method": api['edit']['method'],
                                      "url": api['edit']['url']
                                    },
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


  return titleJson