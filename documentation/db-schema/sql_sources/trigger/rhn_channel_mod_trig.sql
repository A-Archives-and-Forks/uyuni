-- created by Oraschemadoc Thu Jan 20 13:57:10 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE TRIGGER "SPACEWALK"."RHN_CHANNEL_MOD_TRIG" 
before insert or update on rhnChannel
for each row
begin
	:new.last_modified := sysdate;
	-- this is a really bad way of saying "if all we''re
	-- changing is the date"
	if updating then
		if (:old.id != :new.id) or
		  (:old.parent_channel != :new.parent_channel) or
		  (:old.org_id != :new.org_id) or
		  (:old.channel_arch_id != :new.channel_arch_id) or
		  (:old.label != :new.label) or
		  (:old.basedir != :new.basedir) or
		  (:old.name != :new.name) or
		  (:old.summary != :new.summary) or
		  (:old.description != :new.description) then
			:new.modified := sysdate;
		end if;
	end if;
end;
ALTER TRIGGER "SPACEWALK"."RHN_CHANNEL_MOD_TRIG" ENABLE
 
/
