-- created by Oraschemadoc Thu Jan 20 13:57:41 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE TRIGGER "SPACEWALK"."RHN_KSSCRIPT_MOD_TRIG" 
before insert or update on rhnKickstartSession
for each row
begin
	:new.modified := sysdate;
end rhn_ksscript_mod_trig;
ALTER TRIGGER "SPACEWALK"."RHN_KSSCRIPT_MOD_TRIG" ENABLE
 
/
