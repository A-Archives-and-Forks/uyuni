Name:           susemanager-schema
Group:          Applications/Internet
Summary:        Oracle SQL schema for Spacewalk server

Version:        1.7.56.22
Release:        1%{?dist}
Source0:        %{name}-%{version}.tar.gz

License:        GPLv2
Url:            http://fedorahosted.org/spacewalk/
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(Digest::SHA)
BuildRequires:  python
Requires:       /sbin/restorecon

Provides:       spacewalk-schema = %{version}
Obsoletes:      rhn-satellite-schema <= 5.1.0

%define rhnroot /etc/sysconfig/rhn/
%define oracle %{rhnroot}/oracle
%define postgres %{rhnroot}/postgres

%description
rhn-satellite-schema is the Oracle SQL schema for the Spacewalk server.
Oracle tablespace name conversions have NOT been applied.

%prep

%setup -q

%build
%if 0%{?fedora} >= 16 || 0%{?suse_version} >= 1110
find . -name '*.91' | while read i ; do mv $i ${i%%.91} ; done
%endif
make -f Makefile.schema SCHEMA=%{name} VERSION=%{version} RELEASE=%{release}
pod2man spacewalk-schema-upgrade spacewalk-schema-upgrade.1
pod2man spacewalk-sql spacewalk-sql.1

%install
rm -rf $RPM_BUILD_ROOT
install -m 0755 -d $RPM_BUILD_ROOT%{rhnroot}
install -m 0755 -d $RPM_BUILD_ROOT%{oracle}
install -m 0755 -d $RPM_BUILD_ROOT%{postgres}
install -m 0644 oracle/main.sql $RPM_BUILD_ROOT%{oracle}
install -m 0644 postgres/main.sql $RPM_BUILD_ROOT%{postgres}
install -m 0644 oracle/end.sql $RPM_BUILD_ROOT%{oracle}/upgrade-end.sql
install -m 0644 postgres/end.sql $RPM_BUILD_ROOT%{postgres}/upgrade-end.sql
install -m 0755 -d $RPM_BUILD_ROOT%{_bindir}
install -m 0755 spacewalk-schema-upgrade $RPM_BUILD_ROOT%{_bindir}
install -m 0755 spacewalk-sql $RPM_BUILD_ROOT%{_bindir}
install -m 0755 -d $RPM_BUILD_ROOT%{rhnroot}/schema-upgrade
cp -r upgrade/* $RPM_BUILD_ROOT%{rhnroot}/schema-upgrade
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp -p spacewalk-schema-upgrade.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p spacewalk-sql.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %{rhnroot}
%{oracle}
%{postgres}
%{rhnroot}/schema-upgrade
%{_bindir}/spacewalk-schema-upgrade
%{_bindir}/spacewalk-sql
%{_mandir}/man1/spacewalk-schema-upgrade*
%{_mandir}/man1/spacewalk-sql*

%changelog
* Fri Mar 02 2012 Jan Pazdziora 1.7.55-1
- Keys for Fedora 16 -- 18.
- Update the copyright year info.

* Thu Mar 01 2012 Milan Zazrivec <mzazrivec@redhat.com> 1.7.54-1
- use pg_dblink_exec to execute insert inside create_pxt_session

* Thu Mar 01 2012 Jan Pazdziora 1.7.53-1
- On Fedora 16, we need to CREATE EXTENSION dblink.

* Thu Mar 01 2012 Jan Pazdziora 1.7.52-1
- Create the dblink* functions during schema upgrade as well.
- lookup_xccdf_profile: schema upgrade (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_xccdf_profile
  (mzazrivec@redhat.com)
- use autonomous_transaction for insert only (mzazrivec@redhat.com)

* Wed Feb 29 2012 Jan Pazdziora 1.7.51-1
- Blend is case sensitive, let's try to play by its rules.
- remove unused data from the rhnUserGroupType table (tlestach@redhat.com)

* Wed Feb 29 2012 Milan Zazrivec <mzazrivec@redhat.com> 1.7.50-1
- lookup_xccdf_ident: schema upgrade (mzazrivec@redhat.com)
- use pg_dblink_exec to execute inserts inside lookup_xccdf_ident
  (mzazrivec@redhat.com)
- use autonomous_transaction for insert only (mzazrivec@redhat.com)
- lookup_xccdf_benchmark: schema upgrade (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_xccdf_benchmark
  (mzazrivec@redhat.com)
- use autonomous_transaction for insert only (mzazrivec@redhat.com)

* Wed Feb 29 2012 Jan Pazdziora 1.7.49-1
- Need to stop blend from attempting to expanding the \i dblink.sql in build
  time.

* Wed Feb 29 2012 Jan Pazdziora 1.7.48-1
- Creating the dblink function(s) upon schema population, in schema public.
- lookup_transaction_package: schema upgrade (mzazrivec@redhat.com)
- use pg_dblink_exec to exec insert inside lookup_transaction_package
  (mzazrivec@redhat.com)
- use autonomous_transaction for insert only (mzazrivec@redhat.com)
- lookup_tag_name: schema upgrade (mzazrivec@redhat.com)
- fix proc dependencies (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_tag_name
  (mzazrivec@redhat.com)
- fix proc dependencies (mzazrivec@redhat.com)
- use autonomous_transaction for insert only (mzazrivec@redhat.com)
- lookup_tag: schema upgrade (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_tag (mzazrivec@redhat.com)
- fix proc dependencies (mzazrivec@redhat.com)
- use autonomous_transaction for insert only (mzazrivec@redhat.com)
- fix sha1 sums (mzazrivec@redhat.com)
- lookup_source_name: schema upgrade (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_source_name
  (mzazrivec@redhat.com)
- fix proc dependencies (mzazrivec@redhat.com)
- use autonomous_transaction in insert only (mzazrivec@redhat.com)

* Wed Feb 29 2012 Jan Pazdziora 1.7.47-1
- fix lookup_config_info return (mzazrivec@redhat.com)
- no need for autonomous_transaction in lookup_snapshot_invalid_reason
  (mzazrivec@redhat.com)
- fix sha1 sum (mzazrivec@redhat.com)
- lookup_package_nevra: schema upgrade (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_package_nevra
  (mzazrivec@redhat.com)
- use autonomous_transaction for insert only (mzazrivec@redhat.com)
- lookup_package_name: schema upgrade (mzazrivec@redhat.com)
- use pg_dblink_exec to exec insert inside lookup_package_name
  (mzazrivec@redhat.com)
- use autonomous_transaction for insert only (mzazrivec@redhat.com)
- fix sha1 sums (mzazrivec@redhat.com)
- lookup_package_delta: schema upgrade (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_package_delta
  (mzazrivec@redhat.com)
- fix sha1 sums (mzazrivec@redhat.com)
- use autonomous_transaction for insert_only (mzazrivec@redhat.com)
- lookup_package_capability: schema upgrade (mzazrivec@redhat.com)
- use pg_dblink_exec to exec insert inside lookup_package_capability
  (mzazrivec@redhat.com)
- use autonomous_transaction for insert only (mzazrivec@redhat.com)

* Tue Feb 28 2012 Jan Pazdziora 1.7.46-1
- fix insert_evr's return (mzazrivec@redhat.com)
- lookup_evr: schema upgrade (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_evr (mzazrivec@redhat.com)
- lookup_evr: use autonomous_transaction for insert only (mzazrivec@redhat.com)
- no need for autonomous_transaction in lookup_erratafile_type
  (mzazrivec@redhat.com)
- lookup_cve: postgresql schema upgrade (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_cve (mzazrivec@redhat.com)
- lookup_cve: oracle schema upgrade (mzazrivec@redhat.com)
- use autonomous_transaction for insert only (mzazrivec@redhat.com)
- we don't need the autonomous_transaction pragma in lookup_config_info anymore
  (mzazrivec@redhat.com)
- update postgresql procs dependencies (mzazrivec@redhat.com)
- lookup_config_info: postgresql schema ugprade (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_config_info
  (mzazrivec@redhat.com)
- lookup_config_info: correct proc dependencies (mzazrivec@redhat.com)
- lookup_config_info: schema upgrade (mzazrivec@redhat.com)
- restrict autonomous_transaction to insert only (mzazrivec@redhat.com)
- create equivalent (empty) files for postgresql (mzazrivec@redhat.com)
- fixing oracle equivalent source sha1s for upgrade scripts 081-092
  (tlestach@redhat.com)

* Mon Feb 27 2012 Simon Lukasik <slukasik@redhat.com> 1.7.45-1
- Correct sha1sum of oracle equivalents (slukasik@redhat.com)

* Mon Feb 27 2012 Simon Lukasik <slukasik@redhat.com> 1.7.44-1
- OpenSCAP integration -- Database schema upgrade. (slukasik@redhat.com)
- OpenSCAP integration -- Database schema. (slukasik@redhat.com)
- update postgresql procs dependencies (mzazrivec@redhat.com)
- use coalesce and proper quoting (mzazrivec@redhat.com)
- lookup_config_filename: postgresql schema upgrade script
  (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_config_filename
  (mzazrivec@redhat.com)
- lookup_config_filename: schema upgrade script (mzazrivec@redhat.com)
- restrict autonomous_transaction to insert only (mzazrivec@redhat.com)
- use 'select into strict' (mzazrivec@redhat.com)
- lookup_client_capability: schema upgrade script (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_client_capability
  (mzazrivec@redhat.com)
- lookup_client_capability: oracle schema upgrade script (mzazrivec@redhat.com)
- restrict autonomous_transaction to insert only (mzazrivec@redhat.com)
- lookup_checksum: schema upgrade files (mzazrivec@redhat.com)
- use pg_dblink_exec to execute insert inside lookup_checksum
  (mzazrivec@redhat.com)
- restrict autonomous_transaction to insert only (mzazrivec@redhat.com)
- pg_dblink_exec: schema upgrade script (mzazrivec@redhat.com)
- weird schema-source-sanity-check.pl checks (mzazrivec@redhat.com)
- fix checksum header (mzazrivec@redhat.com)
- Introduce pg_dblink_exec for executing SQL queries in a separate db
  connection (mzazrivec@redhat.com)

* Mon Feb 27 2012 Jan Pazdziora 1.7.43-1
- All Oracle triggers now have their PostgreSQL counterparts.

* Thu Feb 23 2012 Jan Pazdziora 1.7.42-1
- Since the table rhn_current_alerts is gone, do not attempt to create trigger
  on it.

* Thu Feb 23 2012 Jan Pazdziora 1.7.41-1
- Adding missing PostgreSQL variant of the rhn_checksumtype_mod_trig trigger.
- The table rhn_current_alerts is no longer used, removing.
- Purge the execution of com.redhat.rhn.taskomatic.task.CleanCurrentAlerts from
  taskomatic.

* Wed Feb 22 2012 Jan Pazdziora 1.7.40-1
- Closing filehandles keeps world tidy.
- Avoid segfault on RHEL 5.

* Tue Feb 21 2012 Jan Pazdziora 1.7.39-1
- Adding checks for schema sources content (table names and such).
- Create the trigger rhn_ksscript_mod_trig correctly on the rhnKickstartScript
  table.
- Create the trigger rhn_conffiletype_mod_trig correctly on the
  rhnConfigFileType table.
- Create the trigger rhn_enqueue_mod_trig correctly on the
  rhnErrataNotificationQueue table.
- Create the trigger rhn_channel_package_mod_trig correctly on the
  rhnChannelPackage table.
- Consolidate both rhnChannelCloned triggers to one, add the new.modified
  initialization to the PostgreSQL variant.

* Tue Feb 21 2012 Jan Pazdziora 1.7.38-1
- Table rhnAppInstallInstance no longer used, dropping.
- Table rhnAppInstallSession no longer used, dropping.
- Prepare for dropping rhnAppInstallSession -- no more delete from it in
  rhn_org.
- Prepare for dropping rhnAppInstallSession -- no more delete from it in
  delete_server.
- Table rhnAppInstallSessionData no longer used, dropping.
- Define PostgreSQL triggers in the function - trigger - function - trigger
  order to make checks easier.

* Mon Feb 20 2012 Tomas Lestach <tlestach@redhat.com> 1.7.37-1
- 790803 - add ip6 to rhn_sat_node (tlestach@redhat.com)
- 790803 - add vip6 to rhn_sat_cluster (tlestach@redhat.com)

* Mon Feb 20 2012 Jan Pazdziora 1.7.36-1
- Removing synonyms notification_formats and ntfmt_recid_seq which are not used
  at all.
- Use rhn_command_q_inst_recid_seq instead of the synonym, also drop
  command_queue_instances which is not used at all.
- Use rhn_command_q_comm_recid_seq instead of the synonym, also drop
  command_queue_commands which is not used at all.
- Synonym command_parameter_threshold not used, removing.

* Mon Feb 20 2012 Jan Pazdziora 1.7.35-1
- Removing rhnUser synonym and just using the base web_contact.
- Dropping valid_countries_tl as it is not used in the application.
- Dropping new_user_postop as it is not used anywhere.

* Mon Feb 20 2012 Jan Pazdziora 1.7.34-1
- Harden the schema-source-sanity-check.pl.
- Fix the postgres/procs/delete_server.sql oracle equivalent source sha1.

* Thu Feb 16 2012 Jan Pazdziora 1.7.33-1
- Need to re-create the view.

* Thu Feb 16 2012 Jan Pazdziora 1.7.32-1
- Both oracle/views/views.deps and postgres/views/views.deps are noops by now,
  removing.
- The view rhnOrgChannelFamilyPermissions is in common, fixing the deps.
- A fast way to force the preferred_time_zone to be string.
- The view rhn_customer_monitoring is the same on both database backends.
- The view rhnWebContactEnabled can be rewritten to be the same on both
  database backends.
- The view rhnUserChannelFamilyPerms is the same on both database backends.

* Thu Feb 16 2012 Jan Pazdziora 1.7.31-1
- View rhnServerNeededPackageView no longer used after update_cache_for_server
  was removed.

* Thu Feb 16 2012 Jan Pazdziora 1.7.30-1
- Removing note_count column from rhnVisServerGroupOverviewLite.
- View rhnVisServerGroupOverview not used, removing.
- Removing note_count column from rhnServerOverview.
- Removing note_count column from rhnServerGroupOverview.

* Wed Feb 15 2012 Jan Pazdziora 1.7.29-1
- No SHA1 of Oracle source in common files.
- Catch situations when common or Oracle files claim SHA1 of Oracle source.
- Adding oracle equivalent source sha1.
- The rhnHistoryView* views do not seem to be used, removing.

* Wed Feb 15 2012 Jan Pazdziora 1.7.28-1
- When upgrading from 1.6, the (smallint, numeric) variant is no longer there.

* Tue Feb 14 2012 Jan Pazdziora 1.7.27-1
- Regenerate rhn_contact_monitoring.
- Regenerate rhnWebContactDisabled.
- Regenerate rhnVisServerGroupMembership.
- Regenerate rhnUserChannelTreeView.
- Regenerate rhnUserChannel.
- Regenerate rhnUserActionOverview.
- Regenerate rhnSharedChannelView.
- Regenerate rhnSharedChannelTreeView.
- Regenerate rhnServerGroupOVLiteHelper.
- Regenerate rhnServerGroupMembership.
- Regenerate rhnOrgChannelTreeView.
- Regenerate rhnOrgChannelFamilyPermissions.
- Regenerate rhnChannelTreeView.
- Regenerate rhnChannelPermissions.
- Regenerate rhnChannelFamilyServers.
- Regenerate rhnActionOverview.
- Fix wrong Oracle source SHA1 values.
- properly mark the delete probe (mzazrivec@redhat.com)
- forgotten trigger: time_series_purge_mod_trig (mzazrivec@redhat.com)
- schema upgrade: cast columns to correct data type (numeric)
  (mzazrivec@redhat.com)
- delete orphaned monitoring data during schema upgrade (mzazrivec@redhat.com)
- rename upgrade script to avoid numbering conflict (mzazrivec@redhat.com)
- rename scripts to avoid number conflicts (mzazrivec@redhat.com)
- time_series revamped: schema upgrade (mzazrivec@redhat.com)
- time_series revamped: new schema (mzazrivec@redhat.com)
- Fixing typo in schema upgrade script; also, rhnServerOverview is not database
  specific.

* Tue Feb 14 2012 Jan Pazdziora 1.7.26-1
- Fixing whitespaces, replacing spaces with tabs.
- Silence NOTICEs and stuff.
- The types directories are no more.
- The user_group_id_t, user_group_label_t, and user_group_name_t no longer
  used, removing.
- Removing rhnUserTypeArray which is no longer used.
- The id_join, label_join, and name_join no longer used, removing.
- Removing rhnUserTypeCommaView which is no longer used.

* Wed Feb 08 2012 Jan Pazdziora 1.7.25-1
- Use rhn_user.role_names instead of rhnUserTypeCommaView.

* Tue Feb 07 2012 Jan Pazdziora 1.7.24-1
- The delete_server proc is the last unverified source file.
- PostgreSQL rhn_config_channel schema is equivalent to Oracle package body.
- PostgreSQL rhn_server schema is equivalent to Oracle package body.
- Creating the schema (for the package) goes into .pks.
- Package rhn_date_manip only exists in Oracle and not used, removing.
- No need to create the stub functions, PostgreSQL will compile stuff on-demand
  anyway.
- Fixing typo in the stub exception message.
- Removing get_org_for_config_content and set_org_quota_total from rhn_quota as
  it is not used.

* Mon Feb 06 2012 Jan Pazdziora 1.7.23-1
- PostgreSQL packages have the same dependencies as the Oracle ones.
- Fixing typo.
- Removing the last three occurrences of rhn_set.set_iterator, and the whole
  package.
- None of the files listed in the .gitignore exists or is produced, removing.
- The header.txt file does not seem to be used anywhere, removing.

* Wed Feb 01 2012 Jan Pazdziora 1.7.22-1
- Fixing oracle equivalent source sha1.

* Wed Feb 01 2012 Miroslav Suchý 1.7.21-1
- rip off SNMP notification method

* Wed Jan 25 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.20-1
- 756918 - fix data for package_group

* Mon Jan 23 2012 Jan Pazdziora 1.7.19-1
- Dropping rhn_bl_obs_mod_trig_fun which was not dropped when
  rhnBlacklistObsoletes was being removed.

* Mon Jan 23 2012 Jan Pazdziora 1.7.18-1
- Drop any three-parameter rhn_prepare_install.

* Mon Jan 23 2012 Jan Pazdziora 1.7.17-1
- 783223 - we need to drop the original smallint-ish functions.

* Mon Jan 23 2012 Jan Pazdziora 1.7.16-1
- 783223 - We need to regenerate rhn_install_satellite and rhn_prepare_install.

* Mon Jan 23 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.15-1
- 756918 - fix data for package_group

* Wed Jan 18 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.14-1
- drop old refresh_newest_package prototype

* Tue Jan 17 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.13-1
- fixed checksums

* Tue Jan 17 2012 Michael Mraka <michael.mraka@redhat.com>
- fixed checksums

* Tue Jan 17 2012 Jan Pazdziora 1.7.11-1
- 782430 - avoid no_data_found from propagating out.

* Tue Jan 17 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.10-1
- enhanced procedure refresh_newest_package

* Tue Jan 17 2012 Jan Pazdziora 1.7.9-1
- Fully qualify the rhn_cache.update_perms_for_user call.

* Mon Jan 16 2012 Miroslav Suchý 1.7.8-1
- Revert "Avoing rhnChecksum_seq.nextval Oracle syntax."
- Revert "Avoid using CURRENT_ALERTS_RECID_SEQ.NEXTVAL Oracle syntax."

* Fri Jan 13 2012 Miroslav Suchý 1.7.7-1
- Avoid using CURRENT_ALERTS_RECID_SEQ.NEXTVAL Oracle syntax.
- Avoing rhnChecksum_seq.nextval Oracle syntax.

* Fri Jan 13 2012 Tomas Lestach <tlestach@redhat.com> 1.7.6-1
- 701767 - fixing sha1 of PG upgrade file (tlestach@redhat.com)

* Fri Jan 13 2012 Tomas Lestach <tlestach@redhat.com> 1.7.5-1
- 701767 - an org shall access a channel even with a flex entitlement
  (tlestach@redhat.com)

* Fri Jan 06 2012 Jan Pazdziora 1.7.4-1
- Dropping the prune_group procedure with the old prototype.

* Tue Jan 03 2012 Jan Pazdziora 1.7.3-1
- Upon drop, the default must not be specified.

* Tue Jan 03 2012 Jan Pazdziora 1.7.2-1
- Prevent output from being printed out for the second time to STDERR upon
  error, for direct mode.

* Mon Jan 02 2012 Jan Pazdziora 1.7.1-1
- The rhn_entitlements.set_group_count is always called with type S in our
  code, removing the user group calls.

* Thu Dec 22 2011 Jan Pazdziora 1.6.42-1
- Fix typo in source file name, add oracle equivalent source sha1.

* Wed Dec 21 2011 Tomas Lestach <tlestach@redhat.com> 1.6.41-1
- update rhn_tasko_run_id_seq sequence number according to
  rhn_tasko_template_id_seq (tlestach@redhat.com)

* Wed Dec 21 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.40-1
- update sha1 sums
- update copyright info

* Wed Dec 14 2011 Jan Pazdziora 1.6.39-1
- For select_direct, print out immediatelly.

* Tue Dec 06 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.38-1
- pgsql schema upgrade: syntax fix & fix index names

* Mon Dec 05 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.37-1
- pgsql: consistent unique constraints
- pgsql: consistent not null constraint

* Fri Dec 02 2011 Jan Pazdziora 1.6.36-1
- 633975 - mark probe as updated if server IP address changed.

* Fri Dec 02 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.35-1
- schema sanity check: use newer Digest::SHA module

* Fri Dec 02 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.34-1
- spacewalk-sql: use exec to launch psql in direct mode
- schema upgrade: run spacewalk-sql in direct mode
- pgsql schema upgrade fix

* Thu Dec 01 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.33-1
- update oracle equivalent sha1 sums

* Wed Nov 30 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.32-1
- pgsql: schema upgrade fixes

* Tue Nov 29 2011 Miroslav Suchý 1.6.31-1
- IPv6: in tables rhnRam, rhnCpu and rhnServerDMI allow only one record per
  server
- IPv6: insert id from sequence using trigger
- IPv6: get_hw_info_as_clob schema upgrade script (mzazrivec@redhat.com)
- IPv6: upgrade script for rhn_server.pkb (mzazrivec@redhat.com)
- IPv6: schema upgrade
- IPv6: get_hw_info_as_clob: adapt to IPv6 changes (mzazrivec@redhat.com)
- IPv6: update rhn_server.get_ip_address() to reflect IPv6 changes
  (mzazrivec@redhat.com)
- IPv6: schema change

* Fri Nov 25 2011 Jan Pazdziora 1.6.30-1
- Fix the in out parameter handling.

* Wed Nov 23 2011 Jan Pazdziora 1.6.29-1
- Fixing wrong plpgsql code.

* Wed Nov 16 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.28-1
- pgsql: varchar2 -> varchar

* Fri Nov 04 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.27-1
- 679335 - store osa-dispatcher jabber password in DB

* Thu Nov 03 2011 Jan Pazdziora 1.6.26-1
- On PostgreSQL, use varchar instead of varchar2.

* Wed Nov 02 2011 Tomas Lestach <tlestach@redhat.com> 1.6.25-1
- introducing name for scripts in kickstart profiles in the webinterface
  (berendt@b1-systems.de)

* Thu Oct 20 2011 Miroslav Suchý 1.6.24-1
- 745102 - add missing constraint to upgrade script

* Wed Oct 19 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.23-1
- fixed rhnContentSourceFilter upgrade to match freshly created table

* Tue Oct 18 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.22-1
- rhnContentSourceFilter stores package filters for repos

* Thu Oct 13 2011 Jan Pazdziora 1.6.21-1
- Unspecified SHA1s have to be reported for upgrades.

* Tue Oct 11 2011 Miroslav Suchý 1.6.20-1
- 745102 - add ip6addr column to rhnServerNetwork

* Fri Sep 30 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.19-1
- 741782 - fixed data types in view

* Tue Sep 27 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.18-1
- drop function must be inside package body
- fixed table alias in update query
- fixed clear_subscriptions() call with optional parameters

* Fri Sep 23 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.17-1
- synced rhn_channel with oracle
- synced rhn_entitlement with oracle

* Thu Sep 15 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.16-1
- 529064 - fixed update_needed_cache which wrongly updated cache if a package
  was in more erratas

* Fri Sep 09 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.15-1
- added EPEL to the list of package providers
- added rpm signing keys for F15, CentOS 6, Scientfic Linux 6 and EPEL

* Wed Sep 07 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.14-1
- create constraints out of table so new and upgraded schemas are equal

* Tue Sep 06 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.13-1
- rhn_command_queue_instances.recid is not smallint anymore

* Fri Sep 02 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.12-1
- upgrade scripts for SMALLINT -> NUMERIC
- upgrade script for FLOAT -> NUMERIC fix
- don't translate NUMBER(X) to SMALLINT or FLOAT

* Wed Aug 31 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.11-1
- removed obsoleted warning
- Fedora 15 needs explicit BuildRequires for python

* Tue Aug 30 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.10-1
- fixed rhnReleaseChannelMap upgrade from 0.5 to 0.6

* Tue Aug 30 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.9-1
- fixed rhn_command upgrade for schema <0.6
- upgrade script for rhn_service_probe_origins
- create contraint and its index at once
- specify NOLOGGING directly
- added sed script replacement for chameleon

* Wed Aug 17 2011 Tomas Lestach <tlestach@redhat.com> 1.6.8-1
- 722189 - adding upgrade script (tlestach@redhat.com)
- 722189 - omit updates for packages installed in several versions (like
  kernel) (tpapaioa@redhat.com)

* Tue Aug 16 2011 Simon Lukasik <slukasik@redhat.com> 1.6.7-1
- Drop the old function, when creating a new one with different argumeters
  (slukasik@redhat.com)

* Mon Aug 15 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.6-1
- 700385 - schema upgrade scripts
- 700385 - replaced synonym with original table_name
- 700385 - created compatibility views for monitoring
- 700385 - added all_tab_columns compatibility view

* Thu Aug 11 2011 Simon Lukasik <slukasik@redhat.com> 1.6.5-1
- Do not confuse people by filename, this is not an upgrade of package
  (slukasik@redhat.com)
- Apply necessary flex changes needed for submitting
  OrgSoftwareSubscriptions.do (slukasik@redhat.com)

* Thu Aug 11 2011 Tomas Lestach <tlestach@redhat.com> 1.6.4-1
- 722189 - rewrite rhnServerNeededView to reflect all available errata
  (tlestach@redhat.com)

* Wed Aug 10 2011 Jan Pazdziora 1.6.3-1
- We missed ON DELETE CASCADE in the past schema upgrade scripts -- fixing now.

* Fri Jul 29 2011 Jan Pazdziora 1.6.2-1
- Adding empty directory for upgrades to 1.6.

* Fri Jul 29 2011 Jan Pazdziora 1.6.1-1
- When versions match, it really is not an error.

* Fri Jul 15 2011 Jan Pazdziora 1.5.6-1
- 711064 - flip the order of iscsi and iscsiname in the kickstart file.

* Tue May 24 2011 Jan Pazdziora 1.5.5-1
- 679333 - update rhnPushClient when deleting server (mzazrivec@redhat.com)

* Wed Apr 20 2011 Michael Mraka <michael.mraka@redhat.com> 1.5.4-1
- in postgres we should upgrade only the affected function

* Mon Apr 18 2011 Michael Mraka <michael.mraka@redhat.com> 1.5.3-1
- added available_fve_chan_subs to postgresql rhn_channel.pkb

* Mon Apr 18 2011 Jan Pazdziora 1.5.2-1
- Need to have separate schema upgrade for PostgreSQL, we do not process schema
  upgrades with chameleon.

* Fri Apr 15 2011 Jan Pazdziora 1.5.1-1
- Fix the oracle equivalent source sha1s for the weak dependencies schema
  sources.
- The schema upgrade for the weak dependencies is for Spacewalk 1.5.
- database tables for weak dependencies (mc@suse.de)

* Fri Apr 08 2011 Jan Pazdziora 1.4.18-1
- Adding missing rhnErrataBuglistTmp schema upgrade scripts.

* Fri Apr 08 2011 Jan Pazdziora 1.4.17-1
- Add 'from' to Errata and 'href' to ErrataBuglist in database schema
  (ug@suse.de)

* Fri Apr 08 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.16-1
- fixed checksum

* Fri Apr 08 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.15-1
- added schema upgrade for rhn_config.pkb on postgresql (PG)
- postgresql doesn't support aliases in update query

* Tue Apr 05 2011 Jan Pazdziora 1.4.14-1
- Forcing strict order of processing in rhn_sg_del_trig, to avoid deadlock.

* Wed Mar 30 2011 Tomas Lestach <tlestach@redhat.com> 1.4.13-1
- 671450 - delete rhel private channel families, if there're no certificate
  entitlements available (tlestach@redhat.com)

* Wed Mar 23 2011 Jan Pazdziora 1.4.12-1
- In update, the column names should not contain table name (PostgreSQL).

* Tue Mar 22 2011 Jan Pazdziora 1.4.11-1
- There is no cursor() function for inline cursors in PostgreSQL, using custom
  function get_hw_info_as_clob instead.

* Thu Mar 10 2011 Jan Pazdziora 1.4.10-1
- Using sequence_nextval instead of the .nextval.
- update database to support SUSE distributions (ug@suse.de)
- suse breed added to ksinstalltype (ug@suse.de)

* Wed Mar 09 2011 Jan Pazdziora 1.4.9-1
- Make the filename absolute so that it works even after we cd to root.

* Fri Mar 04 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.8-1
- added schema upgrade script for rhnBlacklistObsoletes
- removed rhnBlacklistObsoletes table
- created postgresql upgrade script for or rhnVirtualization.uuid index

* Thu Mar 03 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.7-1
- upgrade script for rhnVirtualization.uuid index
- 468690 - added index to rhnVirtualization.uuid

* Fri Feb 25 2011 Jan Pazdziora 1.4.6-1
- Need to return new at the end of a trigger function.

* Thu Feb 24 2011 Jan Pazdziora 1.4.5-1
- Adding a schema upgrade script for the sat_node_probe drop.
- Adding a schema upgrade script for the web_cust_notif_seq drop.

* Wed Feb 23 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.4-1
- schema upgrade script for dropped tables

* Tue Feb 22 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.3-1
- removed unused rhn_sat_node_probe table
- rhn_synch_probe_state doesn't depend on rhn_satellite_state
- removed unused table web_customer_notification

* Fri Feb 18 2011 Jan Pazdziora 1.4.2-1
- Make the index on rhnActionErrataUpdate (action_id, errata_id) unique.

* Mon Feb 07 2011 Jan Pazdziora 1.4.1-1
- Fixed rhn_ugm_applicant_fix_fun trigger function.

* Thu Jan 27 2011 Michael Mraka <michael.mraka@redhat.com> 1.3.18-1
- 671464 - added schema upgrade for new keys 
- added Fedora 14 key
- added Fedora 13 key
- added new Spacewalk key
- 671464 - added RHEL6 key
- For upgrades, missing PostgreSQL equivalent is an error.
- Catch situation when both .sql and .sql.oracle or .sql.postgresql schema
  upgrade scripts exist.

* Tue Jan 25 2011 Jan Pazdziora 1.3.17-1
- Add PostgreSQL schema upgrade scripts for 1.2 -> 1.3 upgrade.

* Fri Jan 21 2011 Jan Pazdziora 1.3.16-1
- The evr_t_as_vre_simple is not available on old Spacewalks, fixed.

* Fri Jan 21 2011 Jan Pazdziora 1.3.15-1
- Changed spacewalk-schema-upgrade to use spacewalk-sql, to run on PostgreSQL.

* Thu Jan 20 2011 Tomas Lestach <tlestach@redhat.com> 1.3.14-1
- updating Copyright years for year 2011 (tlestach@redhat.com)
- The maximum pagesize is 50000 -- this will prevent the headings to be
  repeated. (jpazdziora@redhat.com)
- Add linesize 4000 to allow long enough lines to be returned.
  (jpazdziora@redhat.com)

* Wed Jan 19 2011 Jan Pazdziora 1.3.13-1
- Using array should be faster than appending string.
- Added --select-mode-direct option to print out the sqlplus/psql output right
  when we get it.
- Show --verbose and --select-mode options in usage; also show usage when
  Getopt::Long::GetOptions fails.

* Wed Jan 19 2011 Michael Mraka <michael.mraka@redhat.com> 1.3.12-1
- fixed failed 1.1 -> 1.3 upgrade test

* Tue Jan 18 2011 Jan Pazdziora 1.3.11-1
- The table rhnPackageChangelog is dropped in 103-rhnPackageChangeLog-
  refactoring.sql, no need to alter it here.

* Tue Jan 11 2011 Jan Pazdziora 1.3.10-1
- Add spacewalk-sql which unifies sqlplus and psql invocation.

* Fri Jan 07 2011 Michael Mraka <michael.mraka@redhat.com> 1.3.9-1
- 662563 - rhn_sndpb_pid_ptype_idx was used for rhn_sndpb_probe_id_pk enforcement
- 662563 - rhn_efilectmp_cid_efid_idx was used for rhn_efilectmp_efid_cid_uq enforcement
- 662563 - web_contact_id_oid_cust_luc was used for web_contact_pk enforcement
- 662563 - rhn_package_path_idx was used for rhn_package_id_pk enforcement
- 653510 - deleting a virt host had a virtual entitlement that would not properly
  move its guests to flex entitled if it was available
- 667232 - fixing issue where balancing of guests between flex an regular
  entitlements did would not work correctly, making certificates very difficult
  to activate

* Thu Dec 23 2010 Jan Pazdziora 1.3.8-1
- Mark PostgreSQL rhn_user schema as equivalent to the Oracle package.
- Dropping rhn_user.add_users_to_usergroups as it is now used anymore.
- Dropping rhn_user.remove_users_from_servergroups as it is not used anywhere.

* Thu Dec 23 2010 Jan Pazdziora 1.3.7-1
- Marking PostgreSQL rpm schema equivalent to the Oracle package.
- Fix PostgreSQL rpm.vercmp to handle empty string epoch gracefully.
- Removing vercmpCounter and vercmpResetCounter from rpm package as they are
  not used anywhere.
- Procedure channel_name_join not used anywhere, removing (together with the
  channel_name_t type).
- View rhnUsersInOrgOverview does not use web_user_site_info, fixing the deps.
- Mark postgres/end.sql as equivalent to the oracle variant (even if they do
  different things).
- Function rhn_org.find_server_group_by_type not used anywhere, removing.
- The rhn_package database package is not used, removing.

* Wed Dec 22 2010 Jan Pazdziora 1.3.6-1
- Fixed the rhnPackage.build_time type on PostgreSQL to
  address rhnpush error.

* Tue Dec 14 2010 Jan Pazdziora 1.3.5-1
- 661109 - the schema upgrade script has to have extension .sql.

* Tue Dec 14 2010 Jan Pazdziora 1.3.4-1
- 661109 - fixing issue where channel subscription would not use a flex guest
  subscription if the system already was using  a flex guest subscription for a
  different channel (jsherril@redhat.com)

* Wed Dec 01 2010 Jan Pazdziora 1.3.3-1
- 650129 - don't change last_modified values during schema upgrade
  (mzazrivec@redhat.com)
- drop unused rhnDaemonState table (tlestach@redhat.com)

* Mon Nov 22 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.2-1
- 655509 - fixed namespace

* Thu Nov 18 2010 Lukas Zapletal 1.3.1-1
- Replacing rownum with limit-offset syntax 
- 645694 - introducing cleanup-packagechangelog-data task 
- Bumping package versions for 1.3. 

* Sun Nov 14 2010 Tomas Lestach <tlestach@redhat.com> 1.2.69-1
- create oracle compatible set of 'instr' functions for postgres(PG)
  (tlestach@redhat.com)

* Sat Nov 13 2010 Tomas Lestach <tlestach@redhat.com> 1.2.68-1
- better call stored functions with correct parameter order
  (tlestach@redhat.com)

* Fri Nov 12 2010 Tomas Lestach <tlestach@redhat.com> 1.2.67-1
- remove 2 extra params from the stored proc and include oracle equivalent sha1
  (tlestach@redhat.com)
- fix typo: rh_config -> rhn_config (tlestach@redhat.com)
- change filemode_in type in stored proc to match the DB type
  (tlestach@redhat.com)

* Thu Nov 11 2010 Lukas Zapletal 1.2.66-1
- Putting packages/rhn_org.pkb in sync with ORA (PG)

* Wed Nov 10 2010 Lukas Zapletal 1.2.65-1
- Adding missing PLSQL function update_needed_cache (PG)

* Wed Nov 03 2010 Jan Pazdziora 1.2.64-1
- correct the rule for rhnUser (mzazrivec@redhat.com)
- define rhnUser as a view of web_customer (mzazrivec@redhat.com)

* Tue Nov 02 2010 Jan Pazdziora 1.2.63-1
- Update copyright years in schema/.

* Tue Nov 02 2010 Jan Pazdziora 1.2.62-1
- Generally, we use sequence_nextval when populating tables, we will just
  require it for all tables.
- Removing sqlplus-specific pieces.
- Replace sysdate with current_timestamp now that common/data is not processed
  by chameleon.
- Replace .nextval notation with sequence_nextval now that common/data is not
  processed by chameleon.
- Turn off chameleon processing for common/data.
- Merging the db-specific data/ sources to common/data.
- fixed typo in upgrade script (tlestach@redhat.com)
- Fixing typo in comment.
- Cannot use the .nextval notation in PostgreSQL sources (which became
  .sequence_nextval with the previous substitution).
- Replace sydate with current_timestamp in Oracle sources.
- Replace nextval with sequence_nextval in PostgreSQL sources.
- Replace .nextval with sequence_nextval in Oracle sources.
- Fixed the oracle equivalent source sha1 of rhnTaskoSchedule.sql.

* Mon Nov 01 2010 Tomas Lestach <tlestach@redhat.com> 1.2.61-1
- adding new TimeSeriesCleanUp taskomatic task (tlestach@redhat.com)

* Mon Nov 01 2010 Tomas Lestach <tlestach@redhat.com> 1.2.60-1
- 645702 - adding upgrade script for delete_errata procedure
  (tlestach@redhat.com)
- updating sha1 in postgres procs/delete_errata.sql file (tlestach@redhat.com)

* Mon Nov 01 2010 Tomas Lestach <tlestach@redhat.com> 1.2.59-1
- 645702 - remove rhnPaidErrataTempCache temporary table (tlestach@redhat.com)

* Mon Nov 01 2010 Jan Pazdziora 1.2.58-1
- Missed drop of rhnSatelliteChannelFamily in schema upgrades, dropping now.

* Fri Oct 29 2010 Jan Pazdziora 1.2.57-1
- The Oracle version and use of find_compatible_sg was changed in
  b6832310938382e6f4e0f3c2d26807f4594ae96d, the comment no longer true.
- Move the source of find_compatible_sg up in the file, to match the position
  of the Oracle code.
- Apply change 15c8aa97447223934e3e9c991b76deef466b0b9b to PostgreSQL code.
- We have rhn_snapshotpkg_sid_nid_uq, no need to have another index on column
  snapshot_id.
- We have rhn_sprofile_id_oid_bc_idx and rhn_server_profile_noid_uq, so
  rhn_server_profile_o_id_bc_idx is not useful, removing.
- Clearing the ancient changelogs for rhn_channel.
- Removing rhnSatelliteChannelFamily as it is no longer referenced.
- Fixing dependencies for rhnRepoRegenQueue.
- No need to have index which includes column which is in primary key and the
  first two which are in rhn_pkgnevra_nid_eid_paid_uq.

* Wed Oct 27 2010 Lukas Zapletal 1.2.56-1
- Addresing recursion with opened cursor in PostgreSQL 
- Function unsubscribe_server now in sync with Oracle 
- Function numtodsinterval now accepts days, minutes, hours (incl. fix)
  

* Mon Oct 25 2010 Lukas Zapletal 1.2.55-1
- Taskomatic schedule schema correction (sysdate)

* Mon Oct 25 2010 Lukas Zapletal 1.2.54-1
- Taskomatic data being inserted in PostgreSQL schema now
- Default cast fix for PostgreSQL

* Mon Oct 25 2010 Jan Pazdziora 1.2.53-1
- Fix dependencies for rhnUserReceiveNotifications.

* Fri Oct 22 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.52-1
- removed unused views
- reviewed more indexes

* Fri Oct 22 2010 Tomas Lestach <tlestach@redhat.com> 1.2.51-1
- 529064 - fixed update_needed_cache which wrongly updated cache if a package
  was in more erratas (michael.mraka@redhat.com)
- We cannot touch old if tg_op is INSERT. (jpazdziora@redhat.com)
- Use uniform eight character indents; clean trailing blanks.
  (jpazdziora@redhat.com)

* Fri Oct 22 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.50-1
- reviewed indexes
- rhnPrivateErrataMail is unused; dropping

* Thu Oct 21 2010 Jan Pazdziora 1.2.49-1
- Need to add date_diff_in_days to schema upgrade scripts.
- Missed the rhnPackageChangeLog view from schema upgrades, fixing.
- Fixing the rhn_pkg_cld_id_seq update for situations when there is no data in
  rhnPackageChangeLogData.

* Wed Oct 20 2010 Lukas Zapletal 1.2.48-1
- Trigger rhn_server_group_org_mapping_fun was missing return clause
- Reformat of rhnServerGroupMembers.sql prior to next change
- PostgreSQL function array_upper returns NULL on empty array
  

* Wed Oct 20 2010 Jan Pazdziora 1.2.47-1
- Dropping rhn_package_changelog_id_trig. The id is always specified explicitly
  (it seems).
- Fixing the SHA1 mapping.
- Schema upgrade script for the new trigger on rhnPackageChangeLogRec.
- Move the triggers from rhnPackageChangeLog to rhnPackageChangeLogRec.

* Wed Oct 20 2010 Jan Pazdziora 1.2.46-1
- Process in chunks of 10000 packages, so that we do not blow the undo
  tablespace.
- Schema upgrade script for the rhnPackageChangeLog refactoring.
- Replace the rhnPackageChangeLog table with compatibility view, so that we do
  not have to rewrite code which just reads the table.
- To save space for rhnPackageChangeLog data, split the table to two.

* Tue Oct 19 2010 Jan Pazdziora 1.2.45-1
- 644349 - do not update/delete all errata entries when the erratum affects
  multiple channels (tlestach@redhat.com)
- Fixing the date_diff_in_days source.
- Use numtodsinterval instead of the arithmetics.

* Mon Oct 18 2010 Jan Pazdziora 1.2.44-1
- Remove the timestamptz_minus_int and minus operator -- we want the interval
  issue addressed properly.
- Fixing typo; also making the nextval call hopefully faster by not going to SQL.
- We cannot touch old if tg_op is INSERT.

* Mon Oct 18 2010 Lukas Zapletal 1.2.43-1
- Fixed rhnServerOverview VIEW to return numeric

* Mon Oct 18 2010 Lukas Zapletal 1.2.42-1
- Universal function date_diff_in_days introduced

* Mon Oct 18 2010 Jan Pazdziora 1.2.41-1
- table rhn_host_check_suites has been removed, drop its synonym
  (michael.mraka@redhat.com)
- table rhnSavedSearchType has been removed, drop its sequence
  (michael.mraka@redhat.com)
- table rhnSavedSearch has been removed, drop its sequence
  (michael.mraka@redhat.com)
- table rhnRelationshipType has been removed, drop its sequence
  (michael.mraka@redhat.com)
- table rhnProductLine has been removed, drop its sequence
  (michael.mraka@redhat.com)
- table rhnProduct has been removed, drop its sequence
  (michael.mraka@redhat.com)
- table rhnMessagePriority has been removed, drop its sequence
  (michael.mraka@redhat.com)
- table rhnMessage has been removed, drop its sequence
  (michael.mraka@redhat.com)
- table rhnMessageType has been removed, drop its sequence
  (michael.mraka@redhat.com)
- table rhnMonitor has been removed, drop its sequence
  (michael.mraka@redhat.com)
- table rhnMonitorGranularity has been removed, drop its sequence
  (michael.mraka@redhat.com)
- table rhnGrailComponents has been removed, drop its sequence
  (michael.mraka@redhat.com)

* Mon Oct 18 2010 Jan Pazdziora 1.2.40-1
- fixed typo (michael.mraka@redhat.com)
- fixed index name (michael.mraka@redhat.com)
- rhn_cnp_pid_idx was not removed from schema (michael.mraka@redhat.com)
- fixed ORA-02429: cannot drop index used for enforcement of unique/primary key
  (michael.mraka@redhat.com)
- Default number in Postgresql views is int8 now (lzap+git@redhat.com)
- Added update_neede_cache to Postgresql rhn_server.pkb (lzap+git@redhat.com)
- Postgres rhn_channel.subscribe_server now in sync with Oracle
  (lzap+git@redhat.com)
- Oracle old changelog removed from rhn_channel.pkb (lzap+git@redhat.com)

* Fri Oct 15 2010 Jan Pazdziora 1.2.39-1
- Add support for the update_family_countsYN parameter to
  rhn_entitlements.prune_group.
- Fix PostgreSQL rhn_entitlements.set_group_count to match the Oracle version
  (and have five arguments as well).
- We only need one comps record per channel, adding unique constraint.
- rhn_host_check_suites is unused; dropping (michael.mraka@redhat.com)
- rhnSatelliteServerGroup is unused; dropping (michael.mraka@redhat.com)
- rhnMessageType is unused; dropping (michael.mraka@redhat.com)
- rhnMessagePriority is unused; dropping (michael.mraka@redhat.com)
- rhnMessage is unused; dropping (michael.mraka@redhat.com)

* Thu Oct 14 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.38-1
- 642962 - fixed issue where some of group by columns are null
- fixed build errors
- there are only deletes from rhnServerMessage; dropping
- Mark the PostgreSQL rhn_exception package as equivalent to the Oracle
  version.
- The cursor exception_details not invoked from anywhere besices
  lookup_exception, no need to have it as package interface.
- Merging Oracle rhn_cache.pkb to PostgreSQL version.

* Thu Oct 14 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.37-1
- removed rhnProductLine
- removed rhnSavedSearchType
- removed rhnPackageSense
- removed rhnProduct
- removed rhnMonitorGranularity
- removed rhnServerCacheInfo
- removed rhnSavedSearch
- removed rhnRelationshipType
- removed rhnProductChannel
- removed rhnPathChannelMap
- removed rhnPackageSenseMap
- removed rhnMonitor
- removed rhnGrailComponents
- removed rhnGrailComponentChoices
- removed rhnEmailAddressLog
- removed rhnChannelParent
- removed rhnActionPackageOrder
- Use numeric instead of number in PostgreSQL. 
- reviewed indexes for rhnErrataFileChannelTmp 
- reviewed indexes for rhnErrataFileChannel 

* Wed Oct 13 2010 Lukas Zapletal 1.2.36-1
- Function rhn_channel.subscribe_server now in sync (Pg-Ora)

* Wed Oct 13 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.35-1
- reviewed more indexes

* Wed Oct 13 2010 Jan Pazdziora 1.2.34-1
- Apply necessary flex changes needed for rhn-satellite-activate.
- Removing old changelog entries from rhn_entitlements.pkb source file.
- Rewrite the use of find_compatible_sg to match the one in PostgreSQL sources
  (no out parameter).
- The function find_compatible_sg is only used from within rhn_entitlements, no
  need to have it in the interface (.pks).
- Removing prune_everything procedure as it no longer exists in the Oracle
  sources either.
- Removing old changelog entries from rhn_entitlements.pks source file.
- Add the flex_in and update_family_countsYN to the PostgreSQL version of
  rhn_entitlements.pks (no pkb yet).
- The table rhn_interface_monitoring is not used anywhere (besides deleting
  from it), removing.
- reviewed indexes for rhnCryptoKeyKickstart (michael.mraka@redhat.com)
- The view rhn_host_monitoring just selects from rhnServer, no need to depend
  on three other objects.

* Wed Oct 13 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.33-1
- schema upgrades for deleted tables and indexes
- reviewed and minimized number of indexes 

* Tue Oct 12 2010 Tomas Lestach <tlestach@redhat.com> 1.2.32-1
- 630884 - send errata notifications after errata cache get's regenerated
  (tlestach@redhat.com)
- 642287 - schema upgrade script for rhnChannelNewestPackageView
  (mzazrivec@redhat.com)
- 642287 - restrict rhnChannelNewestPackageView to packages in channels
  (mzazrivec@redhat.com)
- The schema sanity checking now reports (but ignores) if the PostgreSQL
  sources do not report SHA1 of the Oracle equivalent. (jpazdziora@redhat.com)
- there were only deletes from rhnTransaction; removing
  (michael.mraka@redhat.com)
- rhnTransactionElement is not referenced anywhere; removing
  (michael.mraka@redhat.com)
- removing dead rhnActionTransactions table (michael.mraka@redhat.com)
- We need to start processing .pks and .pkb files as well because we will want
  to keep the procedural sources in sync too. (jpazdziora@redhat.com)
- We currently do no have any useful content to put to postgres/start.sql, we
  just silence the sanity checking script. (jpazdziora@redhat.com)
- reviewed indexes for rhnActionErrataUpdate (michael.mraka@redhat.com)
- reviewed indexes for rhnActionConfigRevision (michael.mraka@redhat.com)
- reviewed indexes for rhnActionConfigFileName (michael.mraka@redhat.com)
- The table rhnAllowTrust not used anywhere, removing. (jpazdziora@redhat.com)
- The table rhnEntitlementLog not used anywhere, removing.
  (jpazdziora@redhat.com)
- The table rhnTextMessage not used anywhere, removing. (jpazdziora@redhat.com)
- The table rhn_command_center_state and synonym command_center_state not used
  anywhere, removing. (jpazdziora@redhat.com)
- The table rhn_command_queue_execs_bk and synonym command_queue_execs_bk not
  used anywhere, removing. (jpazdziora@redhat.com)
- The table rhn_command_queue_instances_bk and synonym
  command_queue_instances_bk not used anywhere, removing.
  (jpazdziora@redhat.com)
- The table rhn_schedule_days_norm and synonym schedule_days_norm not used
  anywhere, removing. (jpazdziora@redhat.com)
- reviewed indexes for rhnActionConfigChannel (michael.mraka@redhat.com)

* Tue Oct 12 2010 Jan Pazdziora 1.2.31-1
- 571608 - delete duplicate kickstart_id, package_name_id pairs
  (mzazrivec@redhat.com)

* Fri Oct 08 2010 Lukas Zapletal 1.2.30-1
- Added constriants on all varchar columns to check '' values (pg)
- Fixed inserting of empty varchars instead of NULL

* Fri Oct 08 2010 Tomas Lestach <tlestach@redhat.com> 1.2.29-1
- substitute '' with null (oracle believes it's the same) (tlestach@redhat.com)

* Thu Oct 07 2010 Partha Aji <paji@redhat.com> 1.2.28-1
- 641145: Updated kickstart timezone and install information needed for Rhel 6
  profiles (paji@redhat.com)

* Thu Oct 07 2010 Jan Pazdziora 1.2.27-1
- Since the oracle/procs/lookup_config_info.sql was changed, we need to update
  the SHA1 in the PostgreSQL source.

* Thu Oct 07 2010 Jan Pazdziora 1.2.26-1
- nvl removal for Oracle is not necessary, reverting (lzap+git@redhat.com)
- upgrade script for 2a3a755ed052a0c3435a00d1e6c1c6c9c3ecc470
  (michael.mraka@redhat.com)
- Avoid the integer arithmetics with timestamps in PostgreSQL.
- Upgrade to Satellite 5.1 from older versions put newline to proxy.deactivate
  record; we shall fix it now.

* Tue Oct 05 2010 Jan Pazdziora 1.2.25-1
- Fixed PostgreSQL trigger rhn_channel_access_trig_fun.
- Avoid using rhn_repo_regen_queue_id_seq.nextval Oracle syntax in
  request_repo_regen.
- postgres header comment cleanup (lzap+git@redhat.com)
- old changelogs from Oracle sql script(s) removed (lzap+git@redhat.com)
- Oracle-Postgres schema synchronization (lzap+git@redhat.com)
- The nvl source is PostgreSQL-specific.
- PostgreSQL NVL stored procedure (colin.coe@gmail.com)
- updated rhnServerOverview.sql for Postgres (lzap+git@redhat.com)
- oracle rhnServerOverview old revision log deletion (lzap+git@redhat.com)
- added upgrade script for queue_errata, rhnSNPErrataQueue and
  rhnSNPServerQueue removal (michael.mraka@redhat.com)
- there were only deletes from rhnSNPServerQueue, no inserts/updates; thus
  removing as a dead code (michael.mraka@redhat.com)
- after queue_errata() removal rhnSNPErrataQueue not used anymore
  (michael.mraka@redhat.com)
- removing read queue_errata() from deps (michael.mraka@redhat.com)
- queue_errata() not called anywhere; removing dead procedure
  (michael.mraka@redhat.com)

* Thu Sep 30 2010 Tomas Lestach <tlestach@redhat.com> 1.2.24-1
- 638893 - removing duplicate cert-check-bunch (tlestach@redhat.com)
- Make schema-source-sanity-check.pl happy again. (jpazdziora@redhat.com)
- Update copyright years. (jpazdziora@redhat.com)
- Mark the Oracle source equivalents in our PostgreSQL source files.
  (jpazdziora@redhat.com)
- 634263 - adding upgrade for previous commit (jsherril@redhat.com)
- 634263 - fixing issue where converting host from virt entitled to not, would
  cause guests registered in other orgs to consume a regular entitelment even
  when a flex was available (jsherril@redhat.com)

* Mon Sep 27 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.23-1
- Marked PostgreSQL schema sources that are PostgreSQL-specific.
  (jpazdziora@redhat.com)
- The adler32 function does not seem to be used, removing.
  (jpazdziora@redhat.com)
- 636740 - asterisks in package search fixed (lzap+git@redhat.com)

* Mon Sep 20 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.22-1
- removed sequence used for rhnUserMessageStatus ids

* Tue Sep 14 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.21-1
- reverted "633263 - removed sha384 from list of checksums"

* Tue Sep 14 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.20-1
- 633263 - removed sha384 from list of checksums

* Mon Sep 13 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.19-1
- added upgrade script for rhnUserMessageType

* Thu Sep 09 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.18-1
- upgrade script for rhn_org.pkb

* Thu Sep 09 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.17-1
- dead code cleanup
- 538663 - unset references to to-be-deleted user in rhnConfigRevision

* Tue Sep 07 2010 Jan Pazdziora 1.2.16-1
- The schema upgrade scripts have to have suffix .sql.
- Return the syntax of constraints to the state before Spacewalk 0.5.
- The upgrade script from 0.5 to 0.6 created the constraint
  rhn_ksscript_rawscript_ck without naming it, recreate properly now.
- Also make sure the rhn_ks_type_ck constraint spelling matches the upgrade
  script.
- The upgrade script from 0.3 to 0.4 did not match the constraint definition in
  0.4, fixing.
- Also make sure the rhn_cntgp_rotate_f_ck constraint spelling matches the
  upgrade script.
- In the past, we have changed the rhn_cntgp_rotate_f_ck to use strings instead
  of numbers; now adding the schema upgrade script.
- Upon upgrade from Spacewalk 0.3 to 0.4, we have lost the
  rhn_package_compat_check check, adding back.
- rhn_server.pks upgrade have to go before rhn_channel.pkb
  (michael.mraka@redhat.com)

* Tue Sep 07 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.15-1
- 573630 - implemented update_needed_cache for channel in pl/sql
- fixed upgrade script for rhnPackageUpgradeArchCompat-data
- fixed query for errata mailer

* Mon Sep 06 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.14-1
- one more upgrade compatibility map fix

* Mon Sep 06 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.13-1
- fixed sparc and deb package upgrade compatibility map

* Mon Sep 06 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.12-1
- 573630 - move update_needed_cache implementation to db
- 585965 - rhnServerNeededView rewritten from scratch
- converted dates to ISO format
- 567178 - adding Pacific/Auckland time zone
- 495973 - adding America/Regina time zone

* Thu Sep 02 2010 Jan Pazdziora 1.2.11-1
- Reapply rhn_cache and rhn_org package and rhn_user package and package body,
  to make for clean schema upgrades from 0.2.
- After running the schema upgrade, recompile the PL/SQL objects and check that
  there are no invalid objects left behind.
- add upgrade hint for quartz tables (tlestach@redhat.com)

* Wed Sep 01 2010 Jan Pazdziora 1.2.10-1
- 626741 - do not allow two repos with same label or repository url

* Mon Aug 30 2010 Partha Aji <paji@redhat.com> 1.2.9-1
- Fixed a typo in the column name in rhnKsdata table (paji@redhat.com)
- 627149 - do not return installtime via xmlrpc when not defined
  (tlestach@redhat.com)
- 529232 - add 'no base' and 'ignore missing' options to kickstart
  (coec@war.coesta.com)

* Fri Aug 27 2010 Tomas Lestach <tlestach@redhat.com> 1.2.8-1
- fix errata-cache-bunch template (tlestach@redhat.com)

* Thu Aug 26 2010 Michael Mraka <michael.mraka@redhat.com> 1.2.7-1
- 593896 - schema upgrade script rewritten to pl/sql
- 591291 - rewrite rhnChannelNewestPackageView
- 619337 - making it so that if a packages checksum changes, the channel it is
  will have its repodata regenerated
- location of schema overrides (for oracle) has changed
- 627149 - adding upgrade script for rpm installation dates

* Tue Aug 24 2010 Partha Aji <paji@redhat.com> 1.2.6-1
- removing stray semicolon (jsherril@redhat.com)

* Tue Aug 24 2010 Partha Aji <paji@redhat.com> 1.2.5-1
- Added a number next to the upgrade script to indicate the execution pt..
  (paji@redhat.com)
- 593896 - Moved Kickstart Parition UI logic (paji@redhat.com)

* Tue Aug 24 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.2.4-1
- remove unnecessary comments from resulting schema
- do not schedule repo-sync-bunch by default, sice it is an org task
- add on delete constraint to rhnTaskoRun

* Thu Aug 19 2010 Tomas Lestach <tlestach@redhat.com> 1.2.3-1
- move RepoSyncTask from satellite to organization level (tlestach@redhat.com)
- update description for bunches with arguments (tlestach@redhat.com)

* Tue Aug 17 2010 Justin Sherrill <jsherril@redhat.com> 1.2.2-1
- 619337 - adding trigger to update last_modified date on channel table if the
  checksum of a package changes (jsherril@redhat.com)
- upgrade script for truncateCacheQueue (michael.mraka@redhat.com)
- truncateCacheQueue removed from schema deps (michael.mraka@redhat.com)
- truncateCacheQueue isn't called anywhere (michael.mraka@redhat.com)

* Tue Aug 17 2010 Tomas Lestach <tlestach@redhat.com> 1.2.1-1
- taskomatic schema changes (tlestach@redhat.com)
- new type of errata file: 'OVAL' (mzazrivec@redhat.com)
- fixed 1.1 schema upgrade (michael.mraka@redhat.com)
- Define lookup_checksum in PostgreSQL, needed for satellite-sync.
  (jpazdziora@redhat.com)
- 571608 - fixing schema issue that allowed multiple entries in
  rhnKickstartPackage with the same package name for the same kickstart id
  (jsherril@redhat.com)
- 601626 - adding server-channel arch mapping to support ppc64
  (jsherril@redhat.com)
- bumping package versions for 1.2 (mzazrivec@redhat.com)

* Mon Aug 09 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.30-1
- 601984 - use clob for the concatting operation, to overcome the varchar
  length limit. (jpazdziora@redhat.com)
- 530519 - change ipaddr column from CHAR(16) to VARCHAR(16)
  (msuchy@redhat.com)

* Thu Aug 05 2010 Jan Pazdziora 1.1.29-1
- Be strict about chameleon exit code again.
- Do not invoke chameleon for Oracle sources.

* Thu Aug 05 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.28-1
- 576222 - modify rhn_kstree_mod_trig behavior

* Wed Aug 04 2010 Partha Aji <paji@redhat.com> 1.1.27-1
- Fixed a couple of schema bloopers on config stuff (paji@redhat.com)

* Tue Aug 03 2010 Jan Pazdziora 1.1.26-1
- Chameleon does not support the NULL clause, fix source.

* Tue Aug 03 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.25-1
- Do not depend on cpp when sed works just as well
- The slash is not needed as it causes the create index command to be run for
  the second time, during raw db population
- Underscore is not valid syntax during raw db population
- Empty line in the create table command causes error during raw db population

* Thu Jul 29 2010 Partha Aji <paji@redhat.com> 1.1.24-1
- fixing a few things with the new config changes for symlinks
  (jsherril@redhat.com)
- renamed a couple of upgrade files .. (paji@redhat.com)
- Fixed a small glitch in the upgrade script.. The column name had an extra _
  (paji@redhat.com)
- Config Management schema update + ui + symlinks (paji@redhat.com)

* Thu Jul 29 2010 Jan Pazdziora 1.1.23-1
- The default_db is gone, we need to set the string up for sqlplus to work.

* Wed Jul 28 2010 Jan Pazdziora 1.1.22-1
- The rhnContentSource.sql defines unique index and not constraint, we should
  do the same in schema upgrade scripts.
- Upgrade script for the number(12) -> number changes.
- The return of rhn_prepare_install has to stay smallint.
- Losen the NUMBER(12) to NUMBER, to have foreign keys happy on PostgreSQL,
  while avoiding ORA-01440.
- Revert "Revert "Revert "Fix numeric/smallint incompatible types in
  PostgreSQL."""
- Use the current rhn_channel.pkb in schema upgrade scripts as well.

* Tue Jul 27 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.21-1
- 618219 - more fixes

* Mon Jul 26 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.20-1
- 618219 - update family counts only once per family

* Wed Jul 21 2010 Jan Pazdziora 1.1.19-1
- If PostgreSQL source specifies SHA1 of Oracle source equivalent, we need to
  verify it.
- Match PostgreSQL create_first_org and create_new_org changes to Oracle
  versions from commit 10c8a7dbca8a825639979f5dcb701472dd6b1d55.
- Add 2010 copyright for commit 10c8a7dbca8a825639979f5dcb701472dd6b1d55.
- Remove the EXCLUDE: production, to make the diff against
  oracle/procs/create_first_org.sql smaller.
- Check that Oracle source files have counterparts in PostgreSQL and vice versa
  (ignoring results for now).
- Add basic sanity checking of the consistency of the schema sources.
- schema/spacewalk/postgres/manual/* is not used anywhere, removing.
  (jpazdziora@redhat.com)

* Mon Jul 19 2010 Jan Pazdziora 1.1.18-1
- add missing upgrade for package too
- Remove lines starting with SQL comment, to match what blend does when
  generating main.sql.
- It is necessary to rename the underlying index, not just the constraint.
- The rhn_ccs_uq was never a constraint -- it was a unique index.

* Mon Jul 19 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.17-1
- fix schema repopulation error

* Fri Jul 16 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.16-1
- remove dropped objects from postgresql
- 532423 - device name can be longer than 16 chars

* Fri Jul 16 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.15-1
- made the rhnc_channel upgrade script use the latest sutff
- cleaned up web_customer, rhnPaidOrgs and rhnDemoOrgs
- fixed a couple of typos on  web_customer schema script
- drop unused table rhnOrgInfo
- move column from table rhnOrgInfo to table web_customer
- remove unused column default_group_type, add new colum staging_content

* Mon Jul 12 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.14-1
- rhn_channel depends on rhnChannelFamilyServerFve

* Fri Jul 09 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.13-1
- fixed schema dependencies
* Thu Jul 08 2010 Justin Sherrill <jsherril@redhat.com> 1.1.12-1
- adding upgrade script for rhnAvailableChannels performance issue
  (jsherril@redhat.com)
- 603240 - fixing performance issue with rhnAvailableChannels, since one half
  of the query looks for channels the org owns, and the other half looks for
  channels shared to the org, changing to union all should be no problem
  (jsherril@redhat.com)
- Fixed a stored proc to only look at flex stuff (paji@redhat.com)

* Thu Jul 08 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.11-1
- fixed dependencies on rhnServerFveCapable and rhnChecksumView
- let schema population fail if there are invalid objects
- Made entitlement logic handle flex guests when the host is virt (un)entitled

* Wed Jul 07 2010 Justin Sherrill <jsherril@redhat.com> 1.1.10-1
- allowing satellite-sync to juggle entitlements between flex guest and regular
  entitlement slots if it can (jsherril@redhat.com)

* Fri Jul 02 2010 Jan Pazdziora 1.1.9-1
- bug fixes to repo sync schema upgrades and sql (shughes@redhat.com)
- 526864 - don't allow duplicated rows in rhnServerPackage
  (michael.mraka@redhat.com)
- Triggers that call something in rhn_email package (schema) are not useful
  because we do not have rhn_email.

* Fri Jul 02 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.8-1
- fix index creation and duplicite name of index (msuchy@redhat.com)
- would be much better if it fails with error when something bad happens
  (michael.mraka@redhat.com)

* Fri Jul 02 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.7-1
- table rhnChannelContentSource depends on rhnContentSource (msuchy@redhat.com)
- Match the types of parameters of create_new_user to those given to us by the
  Java code. (jpazdziora@redhat.com)

* Thu Jul 01 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.6-1
- syntax error on rhnContentSource table sql (shughes@redhat.com)
- modify last_synced column for repo sync (shughes@redhat.com)
- missing semicolon on sql declare block (shughes@redhat.com)
- making links between repo objects and taskomatic (shughes@redhat.com)
- migrate sync date from repo content source to the channel table
  (shughes@redhat.com)
- modified repo schema to handle org_id for content source objects. migrate
  script updated too. (shughes@redhat.com)
- adding extra column to the rhnTaskQueue to allow tracking of many2many
  objects IDs (shughes@redhat.com)
- upgrade script for migrating channels from repo table to the new mapping
  table, rhnChannelContentSource (shughes@redhat.com)
- initial table for mapping channel ids to content sources (yum repos)
  (shughes@redhat.com)
- renaming to contentsource since we are moving channel out to a new mapping
  table named rhnChannelContentSource (shughes@redhat.com)
- Fixed a goofed up merge for rhn_channel.pkb (paji@redhat.com)
- Updated the position of rhnPackageRepodata.sql to avoid conflict in naming
  (paji@redhat.com)
- added rhn channels and rhn_entitlements schema upgrade items
  (paji@redhat.com)
- Consolidate virtual instance type changes to 1 file (paji@redhat.com)
- Added code to get multiorgs org -> software channel ents page work with flex
  entitlements (paji@redhat.com)
- Added the convert to flex plsql operation (paji@redhat.com)
- Wiped out unused bulk procs (paji@redhat.com)
- Removed unused stored procedures (paji@redhat.com)
- Added an rhnException data (paji@redhat.com)
- Added channel family permissions to upgrade (paji@redhat.com)
- adding flex guest detection at registration time (jsherril@redhat.com)
- Commiting the initial compilable merge of rhn_channel (paji@redhat.com)
- Added rhnChannelFamilyServerFve in the hopes that it'll get used
  (paji@redhat.com)
- updating rhn_entitlement package for cert activation (jsherril@redhat.com)
- convertin rhn_entitlements.pkb to use four spaces instead of tabs
  (jsherril@redhat.com)
- Updated some views using hosted changes (paji@redhat.com)
- few fixes for rhn cert activation, cert activation now works and populates
  max_members correctly, but not populating fve_max_members yet
  (jsherril@redhat.com)
- matching hosteds column names for flex guests (jsherril@redhat.com)
- first attempt at adding flex guest to sat cert processing
  (jsherril@redhat.com)
- adding flex guest table changes (jsherril@redhat.com)

* Mon Jun 28 2010 Jan Pazdziora 1.1.5-1
- As the tables rhnChannelFamilyLicense and rhnChannelFamilyLicenseConsent were
  removed, so should the triggers.
- Replace nvl and nvl2 with coalesce, to make the rhnServerNeededView view
  compatible with PostgreSQL.
- Revert "Revert "Fix numeric/smallint incompatible types in PostgreSQL.""

* Mon Jun 28 2010 Jan Pazdziora 1.1.4-1
- The for does not like NULL which we get for empty ents_to_process.
- Array concatenation seems to want array_append.
- Fix cursors in PostgreSQL version of prune_group.
- Use AS with column alias.
- TOP declaration seems to be needed, for Makefile to be useful at all.

* Mon Jun 21 2010 Jan Pazdziora 1.1.3-1
- updating rhnPackageRepodata table to not use a reserved word.
  (jsherril@redhat.com)
- Good Bye rhnChannelFamilyLicense and rhnChannelFamilyLicenseConsent tables
  schemas (paji@redhat.com)
- Removed the bulk-subscribe and unsubscribe which is not used anywhere
  (paji@redhat.com)

* Mon May 31 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.2-1
- none of rhnDumpSnapshot* exists anymore
- 585965 - adding upgrade schema for bug
- 585965 - fixing issue with multilib packages and errata-cache generation
- Fix ORA-02429 error during schema upgrade

* Mon Apr 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.1-1
- bumping spec files to 1.1 packages

* Wed Apr 14 2010 Justin Sherrill <jsherril@redhat.com> 0.9.8-1
- moving rhn_schedule_days to be db depedent because it has an inner select
  clause (jsherril@redhat.com)
- 516772 - removing fedora version specific kickstart install types since we do
  not use them (jsherril@redhat.com)

* Tue Apr 13 2010 Jan Pazdziora 0.9.5-1
- Fix Makefile to workaround chameleon failing.

* Mon Apr 12 2010 Miroslav Suchý <msuchy@redhat.com> 0.9.4-1
- Fix db schema for debian support (ukas.durfina@gmail.com)
- Retrieve the rhn_schedules(recid) instead of using the hardcoded value of 1 (jpazdziora@redhat.com)
- schema upgrade for Spacewalk and Fedora gpg keys (michael.mraka@redhat.com)
- 561553 - added Spacewalk into package providers
- drop this useless index (michael.mraka@redhat.com)
- 563902 - tuned sql upgrade script (michael.mraka@redhat.com)

* Thu Mar 11 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.3-1
- fixed misplaced column in index

* Tue Mar 09 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.2-1
- 568293 - don't allow duplicated rows in rhnChecksum
- added constraints to rhnReleaseChannelMap
- repo generation changes, precomputing package repodata

* Thu Feb 18 2010 Miroslav Suchý <msuchy@redhat.com> 0.9.1-1
- support for Debian (lukas.durfina@gmail.com)

* Thu Feb 04 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.9-1
- call update_family_counts() only once in prune_family()

* Wed Feb 03 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.7-1
- fixed upgrades 0.7 -> 0.8

* Mon Feb 01 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.6-1
- 559447 - added upgrade scripts

* Fri Jan 29 2010 Miroslav Suchý <msuchy@redhat.com> 0.8.5-1
- 559447 - speed up rhn-satelite-activate (michael.mraka@redhat.com)
- 559447 - removed update_family_counts() from clear_subscriptions() (michael.mraka@redhat.com)

* Fri Jan 15 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.4-1
- added upgrade script for rhnChannel.checksum_type_id

* Thu Jan 14 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.3-1
- dropped dead tables

* Mon Dec 07 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.2-1
- fixed sha256 related data upgrade scripts

* Fri Dec 04 2009 Michael Mraka <michael.mraka@redhat.com> 0.8.1-1
- SHA256 feature related changes

* Mon Nov 30 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.7.7-1
- schema upgrade fixes for Spacewalk 0.7

* Thu Nov 19 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.6-1
- replaced cursors + for loops with already written bulk procedure
- removed cartesian join
- 532683 - removed unnecessary table joins
- fixed schema upgrades
- optimized queries in update_perms_for_server
- 532683 - optimized delete

* Thu Oct 22 2009 Miroslav Suchy <msuchy@redhat.com> 0.7.5-1
- 449167 - record installation date of rpm package

* Tue Oct 20 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.4-1
- 449167 - record rpm installation date
- 522526 - fixing issue where snippets couldnt be used in the partitioning section of the kickstart wizard (jsherril@redhat.com)
- 522526 - adding schema upgrade script for snippet issue (jsherril@redhat.com)
- Don't indent sql upgrade code in resulting script (mzazrivec@redhat.com)
- 523389 - can't add NOT NULL column into non-empty table (michael.mraka@redhat.com)
- 523389 - decrease TEMP usage (michael.mraka@redhat.com)
- 523389 - add support for schema upgrade overrides (mzazrivec@redhat.com)

* Thu Sep 17 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.3-1
- 523389 - split update into smaller chunks so it will not eat all UNDO at once
- 476851 - removal of tables: rhn_db_environment, rhn_environment (upgrade)
- 476851 - remove environment colum which refers to deleted rhn_enviroment table
- 476851 - removal of tables: rhn_db_environment, rhn_environment

* Wed Sep 02 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.2-1
- Add symlink capability to config management (joshua.roys@gtri.gatech.edu)
- 517867 - insert solaris data only if these do not exist

* Thu Aug 13 2009 Devan Goodwin <dgoodwin@redhat.com> 0.7.1-1
- bumping Version to 0.7.0 (jmatthew@redhat.com)
- Removing PostgreSQL rhnFAQ trigger, table no longer exists.
  (dgoodwin@redhat.com)
- Fix numeric/smallint incompatible types in PostgreSQL. (dgoodwin@redhat.com)
- adding upgrade for new fedora gpg key (jsherril@redhat.com)
- adding newest fedora gpg key, and moving _data sql file to the right place
  (jsherril@redhat.com)

* Thu Aug 06 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.6.21-1
- remove symlinks from schema upgrades
- consistent data in new & upgraded schema
- create or replace function needs to be followed by execute
- remove extraneous execute after create index

* Wed Aug 05 2009 John Matthews <jmatthew@redhat.com> 0.6.20-1
- bugfix patch on selinux config file deploy (joshua.roys@gtri.gatech.edu)
- use new path to merged schema file (mzazrivec@redhat.com)
- fixing schema errors for build (jsherril@redhat.com)

* Wed Aug 05 2009 Jan Pazdziora 0.6.19-1
- updating repo-sync schema to better conform with new schema standards, also
  adding deps (jsherril@redhat.com)
- being cautious (pkilambi@redhat.com)
- Fixing the upgrades to default to sha1 for already existing channels
  (pkilambi@redhat.com)
- fixing small typo in upgrade script names (jsherril@redhat.com)
- Merge branch 'master' into repo-sync (jsherril@redhat.com)
- upgrade script for the previous commit. Patch from Joshua Roys
  (joshua.roys@gtri.gatech.edu)
- Patch: Selinux Context support for config files (joshua.roys@gtri.gatech.edu)
- moving three new tables for postgres merge (jsherril@redhat.com)
- merge conflict (jsherril@redhat.com)
- Re-order Oracle upgrade script. (dgoodwin@redhat.com)
- adding label to ContentSource schema (jsherril@redhat.com)
- merge conflict (jsherril@redhat.com)
- initial yum repo sync schema and UI work (jsherril@redhat.com)

* Wed Jul 29 2009 John Matthews <jmatthew@redhat.com> 0.6.18-1
- Add upgrade scripts for PostgreSQL compat procedures. (dgoodwin@redhat.com)

* Tue Jul 28 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.17-1
- Fix rhnVersionInfo information (jortel@redhat.com)
- Restore some Oracle/PostgreSQL compatability functions.
  (dgoodwin@redhat.com)

* Mon Jul 27 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.16-1
- Add support for PostgreSQL schema. (jortel@redhat.com)
- Build both database versions from common schema. (jortel@redhat.com)
- Add spacewalk-schema BuildRequires for chameleon. (dgoodwin@redhat.com)

* Mon Jul 27 2009 John Matthews <jmatthew@redhat.com> 0.6.15-1
- fixing descritpion on checksums (pkilambi@redhat.com)
-  Sha256 support for channel creation: (pkilambi@redhat.com)

* Wed Jul 22 2009 John Matthews <jmatthew@redhat.com> 0.6.14-1
- 512814 - tickle the upgrade logic (mmccune@redhat.com)

* Thu Jul 16 2009 Miroslav Suchy <msuchy@redhat.com> 0.6.13-1
- 512104 - add sshbannerignore parametr to existing probes which use ssh

* Mon Jul 06 2009 John Matthews <jmatthew@redhat.com> 0.6.12-1
- 509029 - schema/upgrade - update the text used for action type =
  kickstart_guest.initiate (bbuckingham@redhat.com)

* Thu Jun 25 2009 John Matthews <jmatthew@redhat.com> 0.6.11-1
- rebuild 

* Thu Jun 25 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.6.10-1
- 506272 - insert sub4v rows only if they do not exist
- 431673 - reworking rhnServerNeededView for performance fixes.
  (mmccune@gmail.com)
- 492588 - Provide for shared child channels with non-shared parent channels
  (jortel@redhat.com)

* Fri Jun 05 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.9-1
- 503243 - Dropping the is_default column as we now determine the default in
  the app code based on the compatible eus channel instead of jus the default.
  (pkilambi@redhat.com)
- no need to add whitespace to upgrade script (mzazrivec@redhat.com)
- monitoring log files belong to /var/log/nocpulse (mzazrivec@redhat.com)
- 502641 - renaming upgrade script to 119-rhnSystemMigrations.sql
  (bbuckingham@redhat.com)
- 502641 - rhnSystemMigrations remove not null constraints from to/from org ids
  (bbuckingham@redhat.com)
- 498467 - A few changes related to the channel name limit increase.
  (jason.dobies@redhat.com)

* Tue May 26 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.8-1
- 501389 - splitting up virt types none and kvm guests, as well as improving
  virt type names (jsherril@redhat.com)

* Mon May 25 2009 Miroslav Suchy <msuchy@redhat.com> 0.6.7-1
- 502476 - rhn_sat_node should have uniq constraint on column server_id

* Mon May 18 2009 Jan Pazdziora 0.6.6-1
- spacewalk-schema-upgrade: add support for reference files
- 498467 - Forgot to update the create scripts with the new column length
  (jason.dobies@redhat.com)
- Merge branch 'bugs' (jason.dobies@redhat.com)
- 498467 - Increased size of channel name column (jason.dobies@redhat.com)

* Wed May 06 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.5-1
- 499046 - making it so that pre/post scripts can be templatized or not,
  defaulting to not (jsherril@redhat.com)
- alter index needs to be run via execute immediate (mzazrivec@redhat.com)
- 461704 - clean time_series when deleting a server (upgrade script)
  (mzazrivec@redhat.com)
- 461704 - clear time_series when deleting server (mzazrivec@redhat.com)
- 496174 - upgrade to view (mmccune@gmail.com)
- 496174 - view optimization. (mmccune@gmail.com)

* Fri Apr 24 2009 Jan Pazdziora 0.6.4-1
- 497477 - add function based index on time_series for faster probe_id lookups,
  use hint in delete to use it

* Wed Apr 22 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.3-1
- 494976 - adding cobbler systme record name usage to reprovisioning (jsherril@redhat.com)

* Tue Apr 21 2009 Jan Pazdziora 0.6.2-1
- spacewalk-schema-upgrade: other stability and code cleanup changes
- 495869 - label the /var/log/spacewalk/schema-upgrade based on the SELinux
  policy
- set noparallel if index rhn_snc_speid_idx exists (mzazrivec@redhat.com)
- spacewalk-schema-upgrade: for upgrades from Satellite 5.3.0 up, the starting
  schema name is satellite-schema
- 487319 - restore text input for SNMP Community String field
  (mzazrivec@redhat.com)
- 487319 - text input for "SNMP Community String" field (mzazrivec@redhat.com)

* Wed Apr 15 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.1-1
- 495133 - fixing errata mailer such that mails are only sent for a particular
  channel that was changed (jsherril@redhat.com)
- fix ORA-00955 when creating RHN_SNC_SPEID_IDX (mzazrivec@redhat.com)
- 149695 - Including channel_id as part of rhnErrataQueue table so that
  taskomatic can send errata notifications based on channel_id instead of
  sending to everyone subscribed to the channel. The changes include db change
  to rhnErrataQueue table and backend change to satellite-sync's errata import.
  (pkilambi@redhat.com)
- 485870 - only recalculate the channel family counts once per family.
  (mmccune@gmail.com)
- 494475,460136 - remove faq & feedback code which used customerservice emails.
  (jesusr@redhat.com)
- fixing some index mixups, nologging was left off the base schema for a few
  indexes for 0.5 (jsherril@redhat.com)
- 480060 - schema changes to support errata list enhancements.  Simple
  (mmccune@gmail.com)
- bump Versions to 0.6.0 (jesusr@redhat.com)
- adding missing index for errata cache\ (jsherril@redhat.com)

* Wed Mar 25 2009 Mike McCune <mmccune@gmail.com> 0.5.20-1
-  472595 - forgot the index in the table definition.  was in the upgrade area only

* Thu Mar 19 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.19-1
- 487316 - disallows multiple eus channels to be considered the most recent
- 472595 - fixes for kickstart performance, start porting ks downloads to java
- update rhnUserInfo page_size to 25

* Wed Mar 11 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.5.17-1
- fix typo in index name (upgrade script)
- add sql upgrade part for 466035

* Tue Mar 10 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.5.15-1
- add missing ';' when creating web_user_site_info_wuid

* Mon Mar  9 2009 Milan Zazrivec <mzazrivec@redhat.com> 0.5.14-1
- fix upgrade script dropping parallel query

* Mon Mar 09 2009 Michael Mraka <michael.mraka@redhat.com> 0.5.13-1
- fixed #489319

* Thu Mar 05 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.12-1
- fixing upgrade script to properly update all dependant tables
- Fix bug 474597, schema updated but upgrade script not included.

* Thu Feb 26 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.11-1
- fix comment to avoid confusion with / symbol

* Thu Feb 19 2009 Devan Goodwin <dgoodwin@redhat.com> 0.5.10-1
- 486254 - Fix broken schema population during spacewalk-setup.

* Wed Feb 18 2009 Pradeep Kilambi 0.5.9-1
- minor typo and dep fixes for rhnRepoRegenQueue table 

* Mon Feb 16 2009 Pradeep Kilambi 0.5.8-1
- rhnRepoRegenQueue table for yum repodata regen queue

* Thu Feb 12 2009 Mike McCune <mmccune@gmail.com> 0.5.7-1
- 484312 - massive cleanup of virt types.  getting rid of useless AUTO type.

* Thu Feb 12 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.6-1
- 484964 - increasing the copyright column size

* Thu Feb 12 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.5-1
- move logs from /var/tmp to /var/log/nocpulse

* Wed Feb 11 2009 Milan Zazrivec 0.5.4-1
- fixed multiorg sql upgrade script

* Thu Feb 05 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.3-1
- 443718 - fixing a view mistage and having a query just use the view
- 443718 - improving errata cache calcs when pushing a single errata
- 481671 - rewrote inner query to improve performance.
- 480671 fix for deleting orgs in multiorg env
- fixing some forgotten indexes
- a few schema fixes and test case fixes related to the errata-cache update
- fixing a few test cases
- renaming upgrade script
- upgrade support for multiorg sharing logic
- validate channel is 'protected' when joining to the rhnChannelTrusts table.

* Fri Jan 23 2009 Jan Pazdziora 0.5.2-1
- fix for ORA-01440 error occurring when updating populated table (Michael M.)
- removed s/%{?dist}// substitution with no effect (Milan Z.)
- spacewalk-schema-upgrade: minor cleanup
- spacewalk-schema-upgrade: add support for schema overrides

* Wed Jan 14 2009 Mike McCune <mmccune@gmail.com> 0.4.17-1
- 461162 - correcting to match upgrade scripts

* Wed Jan 14 2009 Milan Zazrivec 0.4.16-1
- fixes for #479950 - spacewalk 0.4: new and upgraded schemas do not match

* Tue Jan 13 2009 Miroslav Suchý <msuchy@redhat.com> 0.4.15-1
- 479837 - Support rpm, which contains files with filename + path longer than 256 chars

* Tue Jan 13 2009 Milan Zazrivec 0.4.13-1
- 461162 - cleanup dead code in systemmanager and add new distro types
- 461162 - more virt-type fixing
- 461162 - get the virtualization provisioning tracking system to work with a :virt system record
- 476730 - increase advisory column to 37

* Wed Jan  7 2009 Milan Zazrivec 0.4.12-1
- added spacewalk-schema-upgrade manual page (bz #479003)
- renamed two sql upgrade scripts to use uniform extension

* Thu Dec 18 2008 Milan Zazrivec <mzazrivec@redhat.com> 0.4.11-1
- fixed duplicate modification of rhnChannel

* Thu Dec 18 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.10-1
- 476644 - fixed rhn_org.delete_user

* Mon Dec 15 2008 Jan Pazdziora 0.4.9-1
- 461162 - adding virt options for cobbler
- 461162 - add type 'auto' virtualization
- remove vmware choice from vm type list
- drop also unique index associated with constraint
- updated the alter script numbers to have things go sequential
- 456532 - initial changes to stored profiles to support multiarch
- initial commit for stored profiles to support multiarch
- fixed upgrade script to upgrade the constraint as well
- added new rhnSet column to clean SQL create scripts
- added upgrade scripts to add necessary column to rhnSet
- updates to rhnRegTokenPackages to include id as primary key as well as sequence for generating ids
- making the arch_id column nullable
- updating rhnRegTokenPackages to include arch_id column
- 461162 - initial commit of the manager layer for cobbler
- changes by multiple authors

* Fri Dec  5 2008 Miroslav Suchý <msuchy@redhat.com> 0.4.8-1
- fix monitoring paths in schema

* Mon Dec  1 2008 Miroslav Suchý <msuchy@redhat.com> 0.4.6-1
- 472910 - fix paths to nofitication configs

* Thu Nov 27 2008 Miroslav Suchy <msuchy@redhat.com> 0.4.5-1
- 473242 - fix paths for alert_queue and ack_queue

* Wed Nov 26 2008 Miroslav Suchy <msuchy@redhat.com> 0.4.4-1
- 473097 - point monitoring paths to new destination

* Fri Nov 21 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.3-1
- resolved #471199 - performance improvement of delete_server

* Fri Oct 31 2008 Miroslav Suchy <msuchy@redhat.com> 0.3.5-1
- 469244 - remove trailing /

* Thu Oct 23 2008 Jan Pazdziora 0.3.4-1
- release containing multiple contributions:
- removed rhn_clean_current_state, is_user_org_admin
- moved /opt dir to proper location
- removed unused $Id$, $id$, and $Log$ in the schema
- removed unused macros from table SQL
- rhn_channel_cloned_comps_trig depends on rhnChannelComps
- changed mode of spacewalk-schema-upgrade
- spacewalk-schema-upgrade: require confirming Enter
- 468016 - remove orphaned rhn_contact_groups in rhn_org.delete_user

* Tue Sep 23 2008 Milan Zazrivec 0.3.3-1
- fixed package obsoletes

* Thu Sep 18 2008 Devan Goodwin <dgoodwin@redhat.com> 0.3.2-1
- Fix bug with bad /var/log/rhn/ permissions.

* Thu Sep 18 2008 Michael Mraka <michael.mraka@redhat.com> 0.2.5-1
- Added upgrade scripts

* Wed Sep 17 2008 Devan Goodwin <dgoodwin@redhat.com> 0.3.1-1
- Bumping version to 0.3.x.

* Wed Sep 10 2008 Milan Zazrivec 0.2.3-1
- fixed package obsoletes

* Tue Sep  2 2008 Devan Goodwin <dgoodwin@redhat.com> 0.2.2-1
- Adding new kickstart profile options.

* Mon Sep  1 2008 Milan Zazrivec <mzazrivec@redhat.com> 0.2.1-1
- bumping version for spacewalk 0.2

* Tue Aug  5 2008 Michael Mraka <michael.mraka@redhat.com> 0.1.0-2
- renamed from rhn-satellite-schema and changed version

* Mon Jun  9 2008 Michael Mraka <michael.mraka@redhat.com> 5.2.0-2
- fixed build issue

* Tue Jun  3 2008 Michael Mraka <michael.mraka@redhat.com> 5.2.0-1
- purged unused code
- rebuilt via brew / dist-cvs

