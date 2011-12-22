-- created by Oraschemadoc Wed Dec 21 14:59:47 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE FORCE VIEW "SPACEWALK"."RHNORGERRATA" ("ORG_ID", "ERRATA_ID", "CHANNEL_ID") AS 
  select
    ac.org_id,
    ce.errata_id,
    ac.channel_id
from
    rhnChannelErrata ce,
    rhnAvailableChannels ac
where
    ce.channel_id = ac.channel_id

 
/
