-- created by Oraschemadoc Tue Jul 19 17:31:29 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE FORCE VIEW "SPACEWALK"."RHNSERVERNEEDEDPACKAGECACHE" ("SERVER_ID", "PACKAGE_ID", "ERRATA_ID") AS 
  select
	server_id,
	package_id,
	max(errata_id) as errata_id
	from rhnServerNeededCache
	group by server_id, package_id
 
/
