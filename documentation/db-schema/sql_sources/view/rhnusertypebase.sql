-- created by Oraschemadoc Thu Apr 21 10:04:15 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE FORCE VIEW "SPACEWALK"."RHNUSERTYPEBASE" ("USER_ID", "TYPE_ID", "TYPE_LABEL", "TYPE_NAME") AS 
  select distinct
    ugm.user_id, ugt.id, ugt.label, ugt.name
from
    rhnUserGroupMembers ugm, rhnUserGroupType ugt, rhnUserGroup ug
where
    ugm.user_group_id = ug.id
and ugt.id = ug.group_type
 
/
