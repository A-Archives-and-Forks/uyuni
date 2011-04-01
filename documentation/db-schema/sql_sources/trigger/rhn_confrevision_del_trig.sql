-- created by Oraschemadoc Thu Jan 20 13:57:18 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE TRIGGER "SPACEWALK"."RHN_CONFREVISION_DEL_TRIG" 
before delete on rhnConfigRevision
for each row
declare
	cursor snapshots is
		select	snapshot_id id
		from	rhnSnapshotConfigRevision
		where	config_revision_id = :old.id;
begin
	for snapshot in snapshots loop
		update rhnSnapshot
			set invalid = lookup_snapshot_invalid_reason('cr_removed')
			where id = snapshot.id;
		delete from rhnSnapshotConfigRevision
			where snapshot_id = snapshot.id
				and config_revision_id = :old.id;
	end loop;
end;
ALTER TRIGGER "SPACEWALK"."RHN_CONFREVISION_DEL_TRIG" ENABLE
 
/
