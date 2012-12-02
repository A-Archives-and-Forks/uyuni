-- oracle equivalent source sha1 d22bbc33269bff042a891bae67e7222390c42f63

create or replace function rhn_solaris_p_mod_trig_fun() returns trigger as
$$
begin
	new.modified = current_timestamp;
 	return new;
end;
$$ language plpgsql;

create trigger
rhn_solaris_p_mod_trig
before insert or update on rhnSolarisPatch
for each row
execute procedure rhn_solaris_p_mod_trig_fun();


