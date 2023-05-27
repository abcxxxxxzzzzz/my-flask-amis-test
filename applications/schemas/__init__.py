from .admin_user import UserOutSchema
from .admin_role import RoleOutSchema
from .admin_power import PowerOutSchema, PowerOutSchema2
from .admin_log import LogOutSchema
from .admin_photo import PhotoOutSchema
from .admin_auth import LoginSchema


# 部门相关序列化
from .live.admin_handicap import HandicapOutSchema
from .live.admin_member import MemberOutSchema,TagOutSchema



# 其他
from .other.admin_title import TitleOutSchema,WeightOutSchema
from .other.admin_domain_https import HTTPSDomainOutSchema