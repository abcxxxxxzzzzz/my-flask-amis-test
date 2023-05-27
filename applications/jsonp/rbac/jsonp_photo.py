# from flask import g

# g.permissions = ['admin:user:show','admin:user:add','admin:user:edit','admin:user:del']

# "hidden": "admin:user:deletea" not in permission
api = {
  "batchDel":  {"method": "delete",  "url": "/admin/photo/batch/$ids",  'permission': 'admin:photo:batch:del'   },
  'list':      {'method': 'get',     'url': '/admin/photo/list'      ,  'permission': 'admin:photo:list'   },
  'show':      {'method': 'get',     'url': '/admin/photo/$id'       ,  'permission': 'admin:photo:show'   },
  'add':       {'method': 'post',    'url': '/admin/photo'           ,  'permission': 'admin:photo:add'   },
  'edit':      {'method': 'put',     'url': '/admin/photo/$id'       ,  'permission': 'admin:photo:edit'   },
  'del':       {'method': 'delete',  'url': '/admin/photo/$id'       ,  'permission': 'admin:photo:del'   },
}     

def getPhotoJson(val):
  permissions = val

  photoJson = {
    "type": "page",
    # "title": "图片管理",
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
                  "url": api['list']['url']
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
                      # "actions": [],
                      "body": {
                        "type": "form",
                        # "api": {
                        #   "method": api['add']['method'],
                        #   "url": api['add']['url']
                        # },
                        "body": [
                          {
                            "type": "input-image",
                            "name": "href",
                            "label": "图片链接",
                            "required": True,
                            "multiple": True,
                            "accept": ".jpg,.png,.gif",
                            "limit": {
                              "maxHeight": 1960,
                              "maxWidth": 4000
                            },
                            "receiver": api['add']['method'] + ":" + api['add']['url'],
                            # "autoFill": {
                            #   "myUrl": "${items|pick:url}",
                            #   "lastUrl": "${items|last|pick:url}"
                            # }
                          },
                        ]
                      }
                    },
                    
                    "align": "left",
                  },
                  "bulkActions",
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
                            "type": "text",
                            "name": "name",
                            "label": "图片名称",
                            "required": True,
                            "align": "center"
                        },
                        {
                            "type": "static-image",
                            "name": "href",
                            "label": "图片",
                            "width": "85px",
                            "height": "50px",
                            "thumbMode": "cover",
                            "enlargeAble": True, # 开启放大
                            "showToolbar": True, # 开启放大图工具
                            "required": True,
                            "align": "center"
                        },
                        {
                            "type": "link",
                            "name": "href",
                            "label": "图片链接",
                            "align": "center",
                            "blank": True,
                            "copyable": True
                        },
                        {
                            "type": "text",
                            "name": "mime",
                            "label": "类型",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "name": "size",
                            "label": "大小",
                            "align": "center"
                        },
                        {
                            "type": "date",
                            "name": "create_time",
                            "label": "上传时间",
                            "align": "center",
                            "format": "YYYY-MM-DD HH:mm:ss"
                        },
                        {
                            "type": "operation",
                            "label": "操作",
                            "align": "center",
                            "fixed": "right",
                            "buttons": [
                                # {
                                #     "label": "编辑",
                                #     "type": "button",
                                #     "actionType": "dialog",
                                #     "level": "link",
                                #     "hidden": "admin:photo:edit" not in permissions,
                                #     "dialog": {
                                #     "title": "编辑",
                                #     "body": {
                                #         "type": "form",
                                #         "api": {
                                #         "method": api['edit']['method'],
                                #         "url": api['edit']['url'],
                                #         },
                                #         "body": [
                                #                 {
                                #                     "type": "input-text",
                                #                     "name": "name",
                                #                     "label": "图片名称",
                                #                     "required": True,
                                #                 },
                                #                 {
                                #                     "type": "input-image",
                                #                     "name": "href",
                                #                     "label": "图片链接",
                                #                     "required": True,
                                #                 },
                                    
                                #         ]
                                #     }
                                #     },
                                #     "id": "u:6e01ac9132f2"
                                # },
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


  return photoJson