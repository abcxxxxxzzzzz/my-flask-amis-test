
menu = {
	"pages": [
		{
			"children": [
                {
                    "label": "首页",
                    "icon": "fa fa-cube",
                    "url": "/",
                    "schema": {
                        "type": "page",
                        "title": "Home",
                        "body": "Home"
                    },
                },
                {
                    "label": "授权管理",
                    "icon": "fa fa-cube",
                    "children": [
                        {
                            "label": "用户管理",
                            "url": "/admin/temp/user",
                            "icon": "fa fa-list",
                            "schemaApi": "get:/admin/user/temp"
                        },
                        {
                            "label": "角色管理",
                            "url": "/admin/temp/role",
                            "icon": "fa fa-plus",
                            "schemaApi": "get:/admin/temp/role"
                        },
                        {
                            "label": "权限管理",
                            "url": "/admin/temp/power",
                            "icon": "fa fa-plus",
                            "schemaApi": "get:/admin/temp/power"
                        },
                        {
                            "label": "日志管理",
                            "url": "/admin/temp/log",
                            "icon": "fa fa-plus",
                            "schemaApi": "get:/admin/temp/log"
                        }
                    ]
                }

			]
		},
	]
}