from flask import g

# g.permissions = ['admin:user:show','admin:user:add','admin:user:edit','admin:user:del']

# "hidden": "admin:user:deletea" not in permission
api = {
  'list':      {'method': 'get',     'url': '/admin/member/list'        , 'permission': 'admin:member:list'  },
  'show':      {'method': 'get',     'url': '/admin/member/$id'         , 'permission': 'admin:member:show'  },
  'add':       {'method': 'post',    'url': '/admin/member'             , 'permission': 'admin:member:add'   },
  'edit':      {'method': 'put',     'url': '/admin/member/$id'         , 'permission': 'admin:member:edit'  },
  'del':       {'method': 'delete',  'url': '/admin/member/$id'         , 'permission': 'admin:member:del'   },
  'download':  {'method': 'get',     'url': '/admin/member'             , 'permission': 'admin:member:batch:add'  }, # 模板
  'batchAdd':  {'method': 'post',    'url': '/admin/member/batch'       , 'permission': 'admin:member:batch:add' },   # 批量添加
  'batchEdit': {'method': 'put',     'url': '/admin/member/batch'       , 'permission': 'admin:member:batch:edit' }, # 批量修改
  'batchDel':  {'method': 'delete',  'url': '/admin/member/batch'       , 'permission': 'admin:member:batch:del'  }, # 批量删除
  


  'recovery':     {'method': 'get',    'url': '/admin/member/recovery'    , 'permission': 'admin:member:recovery'  }, # 回收站
  'recoveryEdit': {'method': 'put',    'url': '/admin/member/recovery'    , 'permission': 'admin:member:recovery'  }, # 还原数据
  'recoveryDel':  {'method': 'delete', 'url': '/admin/member/recovery'    , 'permission': 'admin:member:recovery'  }, # 彻底删除
  
  'handicap':  {'method': 'get',     'url': '/admin/handicap/list'      , 'permission': 'admin:handicap:list'   },  # 获取部门
  'tag':       {'method': 'get',     'url': '/admin/tag/list'           , 'permission': 'admin:tag:list' }          # 标签
}

def getMemberJson(val):
  permissions = val

  memberJson = {
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
                            "hidden": g.user.is_super != 1,
                            "label": "部门",
                            "type": "select",
                            "name": "ids",
                            "size": "md",
                            "mode": "horizontal",
                            "multiple": True,
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
                          {
                            "label": "标签",
                            "type": "select",
                            "name": "tags",
                            "size": "md",
                            "mode": "horizontal",
                            "multiple": True,
                            # "joinValues": False,
                            # "extractValue": True,
                            "searchable": True,
                            "clearable": True,
                            "source": {
                              "method": api['tag']['method'],
                              "url": api['tag']['url'],
                              "responseData": {
                                "options": "${rows|pick:label~name,value~id}"
                              }
                            },
                          },
                          {
                            "type": "input-text",
                            "name": "more",
                            "label": "模糊搜索",
                            "clearable": True,
                            "placeholder": "可搜索会员账户、真实姓名、银行卡号、备注",
                            "size": "full",
                            "mode": "horizontal"
                          },
                    ],

                    # "submitText": "搜索",
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
                        "onClick": "props.formStore.setValues({ids: '', tag: '','more':''});"
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
                      }
                    ]

              },
              {
                "type": "crud",
                "name": "my_crud",
                "syncLocation": False,
                "api": {
                  "method": api['list']['method'],
                  "url": api['list']['url'],
                },
                # "filter": {
                #     "id": "search-more",
                #     "hiddenOn": True,
                #     "title": "多条件搜索",
                #     "body": [
                #       {
                #         "type": "group",
                #         "body": [
                #           {
                #             "label": "部门",
                #             "type": "select",
                #             "name": "ids",
                #             "size": "md",
                #             "multiple": True,
                #             # "joinValues": False,
                #             # "extractValue": True,
                #             "searchable": True,
                #             "clearable": True,
                #             "source": {
                #               "method": api['handicap']['method'],
                #               "url": api['handicap']['url'],
                #               "responseData": {
                #                 "options": "${rows|pick:label~name,value~id}"
                #               }
                #             },
                #           },
                #           {
                #             "type": "input-text",
                #             "name": "search",
                #             "label": "模糊搜素",
                #             "clearable": True,
                #             "placeholder": "可搜索会员账户、真实姓名、银行卡号、联系电话、备注",
                #             "size": "full",
                #             "mode": "horizontal"
                #           },
                #         ]
                #       }
                #     ],
                #     "actions": [
                #       {
                #         "type": "reset",
                #         "label": "重置",
                #         "size": "sm",
                #       },
                #       {
                #         "type": "submit",
                #         "level": "primary",
                #         "label": "查询",
                #         "size": "sm",
                #       },
                #       {
                #         "type": "button",
                #         "level": "default",
                #         "label": "隐藏",
                #         "size": "sm",
                #         "onEvent": {
                #           "click": {
                #             "actions": [
                #               {
                #                 "actionType": "hidden",
                #                 "componentId": "search-more"
                #               }
                #             ]
                #           }
                #         }
                #       }
                #     ]
                # },



                "bulkActions": [
                  # {
                  #   "label": "选中更新",
                  #   "actionType": "ajax",
                  #   "icon": "fa-regular fa-trash-can",
                  #   "level": "danger",
                  #   # "api": "delete:https://3xsw4ap8wah59.cfc-execute.bj.baidubce.com/api/amis-mock/sample/${ids|raw}",
                  #   "hidden": api['batchEdit']['permission'] not in permissions,
                  #   "api": {
                  #     "method": api['batchEdit']['method'],
                  #     "url": api['batchEdit']['url'],
                  #     "data": {
                  #       "ids": "${ids|raw}"
                  #     }
                  #   },
                  #   "confirmText": "确定要批量删?",
                    
                  # },
                  {
                    "label": "选中更新",
                    "actionType": "dialog",
                    "level": "info",
                    "icon": "fa-solid fa-pen-to-square",
                    "type": "button",
                    "hidden": api['batchEdit']['permission'] not in permissions,
                    "dialog": {
                      "title": "选中更新",
                      "closeOnEsc": True,
                      "closeOnOutside": True,
                      "body": {
                        "type": "form",
                        "api": {
                          "method": api['batchEdit']['method'],
                          "url": api['batchEdit']['url'] + "/${ids|raw}",
                        },
                        "body": [
                            # {
                            #     # "hiddenOn": "data.type != 2",
                            #     "label": "部门",
                            #     "type": "select",
                            #     "name": "handicapIds",
                            #     # "size": "md",
                            #     "mode": "horizontal",
                            #     # "multiple": True,
                            #     # "joinValues": False,
                            #     # "extractValue": True,
                            #     "searchable": True,
                            #     "clearable": True,
                            #     "clearValueOnHidden": True,
                            #     "required": True,
                            #     "source": {
                            #       "method": api['handicap']['method'],
                            #       "url": api['handicap']['url'],
                            #       "responseData": {
                            #         "options": "${rows|pick:label~name,value~id}"
                            #       }
                            #     },
                            # },
                            {
                                "type": "select",
                                "name": "type",
                                "label": "更新字段",
                                "align": "center",
                                "required": True,
                                "searchable": True,
                                "clearable": True,
                                # "value": "0",
                                "options": [
                                        {
                                            "label": "备注",
                                            "value": "0"
                                        },
                                        {
                                            "label": "标签",
                                            "value": "1"
                                        },
                                  ]
                            },
                            {
                              "hiddenOn": "data.type != 0",
                              "name": "details",
                              "type": "input-text",
                              "label": "备注",
                              "clearValueOnHidden": True,
                              "required": True,
                            },
                            {
                              "hiddenOn": "data.type != 1",
                              "type": "select",
                              "name": "tagIds",
                              "label": "标签",
                              "align": "center",
                              "required": True,
                              # "size": "full",
                              "multiple": True,
                              "joinValues": False,
                              "extractValue": True,
                              "searchable": True,
                              "clearable": True,
                              "clearValueOnHidden": True,
                              "required": True,
                              "placeholder": "请选择",
                              "source": {
                                "method": api['tag']['method'],
                                "url": api['tag']['url'],
                                "responseData": {
                                  "options": "${rows|pick:label~name,value~id}"
                                }
                              },
                            },
                            
                          
                        ]
                      }
                    },
                  },
                  {
                    "label": "选中删除",
                    "actionType": "ajax",
                    "icon": "fa-regular fa-trash-can",
                    "level": "danger",
                    # "api": "delete:https://3xsw4ap8wah59.cfc-execute.bj.baidubce.com/api/amis-mock/sample/${ids|raw}",
                    "hidden": api['batchDel']['permission'] not in permissions,
                    "api": {
                      "method": api['batchDel']['method'],
                      "url": api['batchDel']['url'],
                      "data": {
                        "ids": "${ids|raw}"
                      }
                    },
                    "confirmText": "确定要批量删除?",
                    
                  },
                ],
                "itemActions": [
                ],
                "features": [
                  "create",
                  "update",
                  "delete",
                ],
                # "filterColumnCount": 3,
                "headerToolbar": [
                  # "filter-toggler",
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
                      "closeOnEsc": True,
                      "closeOnOutside": True,
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
                                      "name": "handicap_id",
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
                                    {
                                      "name": "username",
                                      "label": "会员账号",
                                      "type": "input-text",
                                      "align": "center",
                                      "required": True,
                                      "validations": {
                                        'maxLength': 100,
                                      },
                                      "validationErrors": {
                                              "maxLength": "超出 $1 长度范围",
                                      },
                                    },
                                    {
                                      "name": "realname",
                                      "label": "真实姓名",
                                      "type": "input-text",
                                      "align": "center",
                                      # "required": True,
                                      "validations": {
                                        'maxLength': 50,
                                      },
                                      "validationErrors": {
                                              "maxLength": "超出 $1 长度范围",
                                      },
                                    },
                                    {
                                      "name": "bank",
                                      "label": "银行卡号",
                                      "type": "input-text",
                                      # "required": True,
                                      # "validations": {
                                      #   'maxLength': 50,
                                      # },
                                      # "validationErrors": {
                                      #         "maxLength": "超出 $1 长度范围",
                                      # },
                                    },

                                    # {
                                    #   "name": "iphone",
                                    #   "label": "联系电话",
                                    #   "type": "input-text",
                                    #   # "required": True,
                                    #   # "validations": {
                                    #   #   'maxLength': 11,
                                    #   # },
                                    #   # "validationErrors": {
                                    #   #     "maxLength": "超出 $1 长度范围",
                                    #   # },
                                    # },
                                    {
                                      "type": "select",
                                      "name": "tag_ids",
                                      "label": "标签",
                                      "align": "center",
                                      # "required": True,
                                      # "size": "full",
                                      "multiple": True,
                                      "joinValues": False,
                                      "extractValue": True,
                                      "searchable": True,
                                      "clearable": True,
                                      "placeholder": "请选择",
                                      "source": {
                                        "method": api['tag']['method'],
                                        "url": api['tag']['url'],
                                        "responseData": {
                                          "options": "${rows|pick:label~name,value~id}"
                                        }
                                      },
                                    },
                                    {
                                      "name": "details",
                                      "label": "备注",
                                      "type": "input-text",
                                      "align": "center",
                                      "validations": {
                                        'maxLength': 100,
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
                              "hidden": g.user.is_super != 1,
                              "label": "部门",
                              "type": "select",
                              "name": "id",
                              # "size": "md",
                              "mode": "horizontal",
                              # "multiple": True,
                              # "joinValues": False,
                              # "extractValue": True,
                              "searchable": True,
                              "clearable": True,
                              "clearValueOnHidden": True,
                              # "required": True,
                              "source": {
                                "method": api['handicap']['method'],
                                "url": api['handicap']['url'],
                                "responseData": {
                                  "options": "${rows|pick:label~name,value~id}"
                                }
                              },
                          },
                            {
                                "type": "tpl",
                                "tpl": "表头格式: <p style=\"color: green\">会员账号(必须)  真实姓名  银行卡号  备注</p>"
                            },
                            {
                                "type": "tpl",
                                "tpl": "<p style=\"color: red\">提示: 必须是 .xlsx 结尾文件，不支持添加部门已经存在会员账号,包括回收站内数据</p>"
                            },
                            {
                              "label": "下载模板",
                              "type": "action",
                              "actionType": "download",
                              "hidden": api['download']['permission'] not in permissions,
                              "api": {
                                'method': api['download']['method'],
                                'url': api['download']['url'] + "/templates.xlsx",
                              }
                            },
                        ]
                      }
                    },
                    "align": "left",
                  },
                  {
                    "label": "批量查询",
                    "type": "button",
                    "icon": "fa-solid fa-seedling",
                    "actionType": "dialog",
                    "level": "success",
                    "size": "sm",
                    # "hidden": api['upload']['permission'] not in permissions,
                    "dialog": {
                      "title": "批量查询",
                      "closeOnEsc": True,
                      "closeOnOutside": True,
                      # "actions": [
                      #       {
                      #         "label": "搜索",
                      #         "actionType": "submit",
                      #         "primary": True,
                      #         "type": "button",
                      #         # "close": False
                      #         # "feedback": {
                      #         #   "title": "操作成功",
                      #         #   "body": "xxx 已操作成功"
                      #         # }
                      #       },
                      #   ],
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
                              "label": "批量查询",
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
                    "label": "自定义更新",
                    "type": "button",
                    "icon": "fa-solid fa-pen-to-square",
                    "actionType": "dialog",
                    "level": "warning",
                    "size": "sm",
                    "hidden": api['batchEdit']['permission'] not in permissions,
                    "dialog": {
                      "title": "自定义更新",
                      "closeOnEsc": True,
                      "closeOnOutside": True,
                      "body": {
                        "type": "form",
                        "api": {
                          "method": api['batchEdit']['method'],
                          "url": api['batchEdit']['url']
                        },
                        "body": [
                            {
                                "hidden": g.user.is_super != 1,
                                "label": "部门",
                                "type": "select",
                                "name": "handicapIds",
                                # "size": "md",
                                "mode": "horizontal",
                                # "multiple": True,
                                # "joinValues": False,
                                # "extractValue": True,
                                "searchable": True,
                                "clearable": True,
                                "clearValueOnHidden": True,
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
                              "name": "vips",
                              "type": "textarea",
                              "label": "会员账号",
                              "clearable": True,
                              "showCounter": True,
                              "minRows": 10,
                              "placeholder": "批量精准更新, 一行一个" ,
                              "clearValueOnHidden": True,
                              "required": True,
                            },
                            {
                                "type": "select",
                                "name": "type",
                                "label": "更新字段",
                                "align": "center",
                                "required": True,
                                "searchable": True,
                                "clearable": True,
                                # "value": "0",
                                "options": [
                                        {
                                            "label": "备注",
                                            "value": "0"
                                        },
                                        {
                                            "label": "标签",
                                            "value": "1"
                                        }
                                  ]
                            },
                            {
                              "hiddenOn": "data.type != 0",
                              "name": "details",
                              "type": "input-text",
                              "label": "备注",
                              "clearValueOnHidden": True,
                              "required": True,
                            },
                            {
                              "hiddenOn": "data.type != 1",
                              "type": "select",
                              "name": "tagIds",
                              "label": "标签",
                              "align": "center",
                              "required": True,
                              # "size": "full",
                              "multiple": True,
                              "joinValues": False,
                              "extractValue": True,
                              "searchable": True,
                              "clearable": True,
                              "clearValueOnHidden": True,
                              "required": True,
                              "placeholder": "请选择",
                              "source": {
                                "method": api['tag']['method'],
                                "url": api['tag']['url'],
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
                  "bulkActions",
                  {
                    "label": "垃圾桶",
                    "type": "button",
                    "icon": "fa-regular fa-trash-can",
                    "actionType": "drawer",
                    "level": "danger",
                    "size": "sm",
                    "hidden": api['recovery']['permission'] not in permissions,
                    "drawer": {
                      "title": "垃圾桶",
                      # "size": "lg",
                      "size": "xl",
                      "position": "right",
                      "closeOnEsc": True,
                      "resizable": True,
                      "closeOnOutside":True,
                      "actions": [],
                      # 开始
                      "body": {
                            "type": "crud",
                            "syncLocation": False,
                            "api": {
                              "method": api['recovery']['method'],
                              "url": api['recovery']['url'],
                            },

                            

                            "bulkActions": [
                              {
                                "label": "彻底删除",
                                "actionType": "ajax",
                                "level": "danger",
                                # "api": "delete:https://3xsw4ap8wah59.cfc-execute.bj.baidubce.com/api/amis-mock/sample/${ids|raw}",
                                "hidden": api['recoveryDel']['permission'] not in permissions,
                                "api": {
                                  "method": api['recoveryDel']['method'],
                                  "url": api['recoveryDel']['url'],
                                  "data": {
                                    "ids": "${ids|raw}"
                                  }
                                },
                                "confirmText": "确定要彻底永久删除?",
                                
                              },
                              {
                                "label": "还原数据",
                                "actionType": "ajax",
                                "level": "info",
                                # "api": "delete:https://3xsw4ap8wah59.cfc-execute.bj.baidubce.com/api/amis-mock/sample/${ids|raw}",
                                "hidden": api['recoveryEdit']['permission'] not in permissions,
                                "api": {
                                  "method": api['recoveryEdit']['method'],
                                  "url": api['recoveryEdit']['url'],
                                  "data": {
                                    "ids": "${ids|raw}"
                                  }
                                },
                                "confirmText": "确定要还原数据?",
                                
                              },
                            ],
                            "features": [
                              "create",
                              "update",
                              "delete",
                            ],
                            # "filterColumnCount": 3,
                            "headerToolbar": [
                              "bulkActions",
                              {
                                "type": "columns-toggler",
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
                                      "placeholder": "请输入会员号",
                                      "mini": True,
                                      "addOn": {
                                              "label": "搜索",
                                              "type": "submit"
                                      }
                              },
                            ],
                            
                            "perPageAvailable": [
                              10,
                              20,
                              50,
                              100,
                              200,
                              500,
                              1000,
                              2000,
                            ],
                            "mode": "table",
                            "columns": [
                              {
                                "name": "id",
                                "label": "ID",
                                "type": "text",
                                "align": "center"
                              },
                              {
                                # "hidden": g.user.is_super != 1,
                                "name": "handicap",
                                "label": "部门",
                                "type": "tpl",
                                "tpl": "${handicap.name}",
                                "align": "center",
                                "copyable": True,
                              },
                              {
                                "name": "username",
                                "label": "会员账户",
                                "type": "text",
                                "align": "center",
                                "copyable": True,
                              },
                              {
                                "name": "realname",
                                "label": "真实姓名",
                                "type": "text",
                                "align": "center",
                                "copyable": True,
                              },
                              {
                                "name": "bank",
                                "label": "银行卡号",
                                "type": "text",
                                "align": "center",
                                "copyable": True,
                              },

                              # {
                              #   "name": "iphone",
                              #   "label": "联系电话",
                              #   "type": "text",
                              #   "align": "center",
                              #   "copyable": True,
                              # },
                              {
                                "name": "tag",
                                "label": "彩金标签",
                                "type": "each",
                                "align": "center",
                                "items": {
                                  "type": "tpl",
                                  # "tpl": "<span class='label label-success m-l-sm'><%= data.name %></span>"
                                  "tpl": "<span class=\"cxd-Tag cxd-Tag--normal cxd-Tag--normal--<%= data.color %> cxd-Tag--normal--hasColor\" style=\"margin-right: 2px；margin-left: 5px\"><span class=\"cxd-Tag-text\"><%= data.name %></span></span>"
                                }
                              },
                              {
                                "type": "tpl",
                                "label": "备注",
                                "align": "center",
                                "tpl": "${details|truncate:10}"
                              },

                              {
                                "type": "date",
                                "name": "create_at",
                                "label": "创建时间",
                                "align": "center",
                                "sortable": True,
                                "format": "YYYY-MM-DD HH:mm:ss"
                              },
                              {
                                "type": "date",
                                "name": "update_at",
                                "label": "更新时间",
                                "align": "center",
                                "sortable": True,
                                "format": "YYYY-MM-DD HH:mm:ss"
                              },
                              {
                                "type": "date",
                                "name": "delete_at",
                                "label": "删除时间",
                                "align": "center",
                                "sortable": True,
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
                      # 结束
                    },
                    "align": "right",
                  },
                  {
                    "type": "columns-toggler",
                    "align": "right",
                    "size": "sm",
                  },
                  {
                    "type": "export-excel",
                    "tpl": "导出",
                    "id": "u:adc705a92fe1",
                    "align": "right",
                    "size": "sm",
                    "icon": "fa-solid fa-download",
                    "label": "导出当页",
                    "exportColumns": [
                            {
                              "name": "handicap",
                              "label": "部门",
                              "type": "tpl",
                              "tpl": "${handicap.name}",
                              "align": "center",
                              "copyable": True,
                            },
                            {
                              "name": "username",
                              "label": "会员账号",
                              "type": "text",
                              "align": "center",
                              "copyable": True,
                            },
                            {
                              "name": "realname",
                              "label": "真实姓名",
                              "type": "text",
                              "align": "center",
                              "copyable": True,
                            },
                            {
                              "name": "bank",
                              "label": "银行卡号",
                              "type": "text",
                              "align": "center",
                              "copyable": True,
                            },

                            # {
                            #   "name": "iphone",
                            #   "label": "联系电话",
                            #   "type": "text",
                            #   "align": "center",
                            #   "copyable": True,
                            # },
                            {
                              "type": "tpl",
                              "label": "彩金标签",
                              "tpl": "${tag|pick:name|join}"
                            },
                            {
                              "name": "details",
                              "label": "备注",
                              "type": "text",
                              "align": "center",
                            },

                            {
                              "type": "date",
                              "name": "create_at",
                              "label": "创建时间",
                              "align": "center",
                              "sortable": True,
                              "format": "YYYY-MM-DD HH:mm:ss"
                            },
                            {
                              "type": "date",
                              "name": "update_at",
                              "label": "更新时间",
                              "align": "center",
                              "sortable": True,
                              "format": "YYYY-MM-DD HH:mm:ss"
                            },
                                
                      
                    ]
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
                          "placeholder": "请输入会员号",
                          "mini": True,
                          "addOn": {
                                  "label": "搜索",
                                  "type": "submit"
                          }
                  },
                ],
                
                "perPageAvailable": [
                  10,
                  20,
                  50,
                  100,
                  200,
                  500,
                  1000,
                  2000,
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
                    # "hidden": g.user.is_super != 1,
                    "name": "handicap",
                    "label": "部门",
                    "type": "tpl",
                    "tpl": "${handicap.name}",
                    "align": "center",
                    "copyable": True,
                  },
                  {
                    "name": "username",
                    "label": "会员账号",
                    "type": "text",
                    "align": "center",
                    "copyable": True,
                  },
                  {
                    "name": "realname",
                    "label": "真实姓名",
                    "type": "text",
                    "align": "center",
                    "copyable": True,
                  },
                  {
                    "name": "bank",
                    "label": "银行卡号",
                    "type": "text",
                    "align": "center",
                    "copyable": True,
                  },

                  # {
                  #   "name": "iphone",
                  #   "label": "联系电话",
                  #   "type": "text",
                  #   "align": "center",
                  #   "copyable": True,
                  # },
                  {
                    "name": "tag",
                    "label": "彩金标签",
                    "type": "each",
                    "align": "center",
                    "items": {
                      "type": "tpl",
                      # "tpl": "<span class='label label-success m-l-sm'><%= data.name %></span>"
                      "tpl": "<span class=\"cxd-Tag cxd-Tag--normal cxd-Tag--normal--<%= data.color %> cxd-Tag--normal--hasColor\" style=\"margin-right: 2px\"><span class=\"cxd-Tag-text\"><%= data.name %></span></span>"
                    }
                  },
                  # {
                  #   "name": "details",
                  #   "label": "备注",
                  #   "type": "text",
                  #   "align": "center",
                  # },
                  {
                    "type": "tpl",
                    "label": "备注",
                    "tpl": "${details|truncate:10}"
                  },

                  {
                    "type": "date",
                    "name": "create_at",
                    "label": "创建时间",
                    "align": "center",
                    "sortable": True,
                    "format": "YYYY-MM-DD HH:mm:ss"
                  },
                  {
                    "type": "date",
                    "name": "update_at",
                    "label": "更新时间",
                    "align": "center",
                    "sortable": True,
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
                                      # "required": True,
                                      "disabled": True,
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
                                      "name": "username",
                                      "label": "会员账号",
                                      "type": "input-text",
                                      "align": "center",
                                      "required": True,
                                      "disabled": True,
                                      "validations": {
                                        'maxLength': 100,
                                      },
                                      "validationErrors": {
                                              "maxLength": "超出 $1 长度范围",
                                      },
                                    },
                                    {
                                      "name": "realname",
                                      "label": "真实姓名",
                                      "type": "input-text",
                                      "align": "center",
                                      "hidden": not g.user.is_super,
                                      # "required": True,
                                      "validations": {
                                        'maxLength': 50,
                                      },
                                      "validationErrors": {
                                              "maxLength": "超出 $1 长度范围",
                                      },
                                    },
                                    {
                                      "name": "bank",
                                      "label": "银行卡号",
                                      "type": "input-text",
                                      "hidden": not g.user.is_super,
                                      # "required": True,
                                      "validations": {
                                        'maxLength': 50,
                                      },
                                      "validationErrors": {
                                              "maxLength": "超出 $1 长度范围",
                                      },
                                    },

                                    # {
                                    #   "name": "iphone",
                                    #   "label": "联系电话",
                                    #   "type": "input-text",
                                    #   "hidden": not g.user.is_super,
                                    #   # "required": True,
                                    #   "validations": {
                                    #     'maxLength': 11,
                                    #   },
                                    #   "validationErrors": {
                                    #       "maxLength": "超出 $1 长度范围",
                                    #   },
                                    # },
                                    {
                                      "type": "select",
                                      "name": "tagIds",
                                      "label": "标签",
                                      "align": "center",
                                      # "required": True,
                                      # "size": "full",
                                      "multiple": True,
                                      "joinValues": False,
                                      "extractValue": True,
                                      "searchable": True,
                                      "clearable": True,
                                      "placeholder": "请选择",
                                      "value": "${tag|pick:id}",
                                      "source": {
                                        "method": api['tag']['method'],
                                        "url": api['tag']['url'],
                                        "responseData": {
                                          "options": "${rows|pick:label~name,value~id}"
                                        }
                                      },
                                    },
                                    {
                                      "name": "details",
                                      "label": "备注",
                                      "type": "input-text",
                                      "align": "center",
                                      "validations": {
                                        'maxLength': 100,
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


  return memberJson