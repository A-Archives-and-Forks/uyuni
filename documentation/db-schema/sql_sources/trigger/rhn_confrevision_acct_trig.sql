-- created by Oraschemadoc Fri Mar  2 05:58:05 2012
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE TRIGGER "SPACEWALK"."RHN_CONFREVISION_ACCT_TRIG" 
after insert on rhnConfigRevision
for each row
declare
	org_id number;
	available number := 0;
	added number := 0;
begin
	-- find the current amount of quota available
    begin
	select	cc.org_id id,
			oq.total + oq.bonus - oq.used available,
			content.file_size added
	into	org_id, available, added
	from	rhnConfigContent	content,
			rhnOrgQuota			oq,
			rhnConfigChannel	cc,
			rhnConfigFile		cf
	where	cf.id = :new.config_file_id
			and cf.config_channel_id = cc.id
			and cc.org_id = oq.org_id
            and :new.config_file_type_id = (select id from rhnConfigFileType where label='file')
			and :new.config_content_id = content.id;
    exception
            when no_data_found then
                added := 0;
                available := 0;
    end;
	if added > available then
		rhn_exception.raise_exception('not_enough_quota');
	end if;
end;
ALTER TRIGGER "SPACEWALK"."RHN_CONFREVISION_ACCT_TRIG" ENABLE
 
/
