-- created by Oraschemadoc Thu Jan 20 13:58:40 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE PROCEDURE "SPACEWALK"."DELETE_SERVER_BULK" (
	user_id_in in number
) is
	cursor systems is
		select	s.element id
		from	rhnSet s
		where	s.user_id = user_id_in
			and s.label = 'system_list';
begin
	for s in systems loop
                delete_server(s.id);
	end loop;
end delete_server_bulk;
 
/
