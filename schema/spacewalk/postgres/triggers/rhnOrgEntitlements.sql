-- oracle equivalent source sha1 c813c2b78f3cfc9ed9c5c96039572f78a7973a8f

create or replace function rhn_org_ent_mod_trig_fun() returns trigger as
$$
begin
       new.modified := current_timestamp;
        
       return new;
end;
$$ language plpgsql;

create trigger
rhn_org_ent_mod_trig
before insert or update on rhnOrgEntitlements
for each row
execute procedure rhn_org_ent_mod_trig_fun();

