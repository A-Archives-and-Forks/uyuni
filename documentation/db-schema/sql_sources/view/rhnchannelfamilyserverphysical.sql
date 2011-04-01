-- created by Oraschemadoc Thu Jan 20 13:56:11 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE FORCE VIEW "SPACEWALK"."RHNCHANNELFAMILYSERVERPHYSICAL" ("CUSTOMER_ID", "CHANNEL_FAMILY_ID", "SERVER_ID", "CREATED", "MODIFIED") AS 
  select	rs.org_id			as customer_id,
		rcfm.channel_family_id		as channel_family_id,
		rsc.server_id			as server_id,
		rsc.created			as created,
		rsc.modified			as modified
	from	rhnChannelFamilyMembers		rcfm,
		rhnServerChannel		rsc,
		rhnServer			rs
	where
		rcfm.channel_id = rsc.channel_id
		and rsc.server_id = rs.id
         and rsc.is_fve = 'N'
        and not exists (
                select 1
                from
                    rhnChannelFamilyVirtSubLevel cfvsl,
                    rhnSGTypeVirtSubLevel sgtvsl,
                    rhnServerEntitlementView sev,
                    rhnVirtualInstance vi
                where
                    -- system is a virtual instance
                    vi.virtual_system_id = rs.id
                    and vi.host_system_id = sev.server_id
                    -- system's host has a virt ent
                    and sev.label in ('virtualization_host',
                                      'virtualization_host_platform')
                    and sev.server_group_type_id = sgtvsl.server_group_type_id
                    -- the host's virt ent grants a cf virt sub level
                    and sgtvsl.virt_sub_level_id = cfvsl.virt_sub_level_id
                    -- the cf is in that virt sub level
                    and cfvsl.channel_family_id = rcfm.channel_family_id
                )
 
/
