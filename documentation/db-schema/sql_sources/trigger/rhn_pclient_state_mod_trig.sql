-- created by Oraschemadoc Thu Jan 20 13:57:53 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE TRIGGER "SPACEWALK"."RHN_PCLIENT_STATE_MOD_TRIG" 
before insert or update on rhnPushClientState
for each row
begin
	:new.modified := sysdate;
end rhn_pclient_state_mod_trig;
ALTER TRIGGER "SPACEWALK"."RHN_PCLIENT_STATE_MOD_TRIG" ENABLE
 
/
