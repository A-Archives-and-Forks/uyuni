-- created by Oraschemadoc Wed Dec 21 14:59:53 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE TRIGGER "SPACEWALK"."RHN_CHANNEL_PACKAGE_MOD_TRIG" 
before insert or update on rhnChannelPackage
for each row
begin
	:new.modified := sysdate;
end rhn_channel_package_mod_trig;
ALTER TRIGGER "SPACEWALK"."RHN_CHANNEL_PACKAGE_MOD_TRIG" ENABLE
 
/
