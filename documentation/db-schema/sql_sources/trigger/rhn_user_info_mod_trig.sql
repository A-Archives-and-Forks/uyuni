-- created by Oraschemadoc Thu Jan 20 13:58:31 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE TRIGGER "SPACEWALK"."RHN_USER_INFO_MOD_TRIG" 
before insert or update on rhnUserInfo
for each row
begin
	:new.modified := sysdate;
end rhn_user_info_mod_trig;
ALTER TRIGGER "SPACEWALK"."RHN_USER_INFO_MOD_TRIG" ENABLE
 
/
