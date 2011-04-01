-- created by Oraschemadoc Thu Jan 20 13:58:59 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE FUNCTION "SPACEWALK"."LOOKUP_PACKAGE_DELTA" (n_in IN VARCHAR2)
RETURN NUMBER
IS
	PRAGMA AUTONOMOUS_TRANSACTION;
	name_id         NUMBER;
BEGIN
	SELECT id INTO name_id
	  FROM rhnPackageDelta
	 WHERE label = n_in;

	RETURN name_id;
EXCEPTION
	WHEN NO_DATA_FOUND THEN
	    INSERT INTO rhnPackageDelta (id, label)
	    VALUES (rhn_packagedelta_id_seq.nextval, n_in)
	    RETURNING id INTO name_id;
	COMMIT;
	RETURN name_id;
END;
 
/
