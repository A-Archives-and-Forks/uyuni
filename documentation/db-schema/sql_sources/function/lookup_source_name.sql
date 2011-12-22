-- created by Oraschemadoc Wed Dec 21 14:59:58 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE FUNCTION "SPACEWALK"."LOOKUP_SOURCE_NAME" (name_in IN VARCHAR2)
RETURN NUMBER
IS
	PRAGMA AUTONOMOUS_TRANSACTION;
	source_id	NUMBER;
BEGIN
        select	id into source_id
        from	rhnSourceRPM
        where	name = name_in;

        RETURN source_id;
EXCEPTION
        WHEN NO_DATA_FOUND THEN
            insert into rhnSourceRPM(id, name)
                    values (rhn_sourcerpm_id_seq.nextval, name_in)
                    returning id into source_id;
            COMMIT;
            RETURN source_id;
END;
 
/
