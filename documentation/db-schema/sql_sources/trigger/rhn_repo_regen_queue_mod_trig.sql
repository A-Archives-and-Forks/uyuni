-- created by Oraschemadoc Tue Jul 19 17:31:33 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE TRIGGER "SPACEWALK"."RHN_REPO_REGEN_QUEUE_MOD_TRIG" 
before insert or update on rhnRepoRegenQueue
for each row
begin
    if :new.id is null then
        select rhn_repo_regen_queue_id_seq.nextval into :new.id from dual;
    end if;
    :new.modified := sysdate;
end;
ALTER TRIGGER "SPACEWALK"."RHN_REPO_REGEN_QUEUE_MOD_TRIG" ENABLE
 
/
