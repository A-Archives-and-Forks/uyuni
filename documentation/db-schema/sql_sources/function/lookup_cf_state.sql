-- created by Oraschemadoc Wed Dec 21 14:59:57 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE FUNCTION "SPACEWALK"."LOOKUP_CF_STATE" (
	label_in in varchar2
) return number deterministic
is
	state_id number;
begin
	select	id
	into	state_id
	from	rhnConfigFileState
	where	label = label_in;

	return state_id;
end;
 
/
