-- created by Oraschemadoc Tue Jul 19 17:31:33 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE TRIGGER "SPACEWALK"."RHN_SNAPCHAN_MOD_TRIG" 
before insert or update on rhnSnapshotChannel
for each row
begin
	update rhnSnapshot set modified = sysdate where id = :new.snapshot_id;
end;
ALTER TRIGGER "SPACEWALK"."RHN_SNAPCHAN_MOD_TRIG" ENABLE
 
/
