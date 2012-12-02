%if 0%{?suse_version}
%define www_path /srv/
%define apache_user wwwrun
%define apache_group www
%else
%define www_path %{_var}
%define apache_user apache
%define apache_group apache
%endif

Name: spacewalk-web
Summary: Spacewalk Web site - Perl modules
Group: Applications/Internet
License: GPLv2
Version: 1.9.4
Release: 1%{?dist}
URL:          https://fedorahosted.org/spacewalk/
Source0:      https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: perl(ExtUtils::MakeMaker)
%if 0%{?suse_version}
BuildRequires: apache2
%endif

%description
This package contains the code for the Spacewalk Web Site.
Normally this source RPM does not generate a %{name} binary package,
but it does generate a number of sub-packages.

%package -n spacewalk-html
Summary: HTML document files for Spacewalk
Group: Applications/Internet
Requires: httpd
Requires: spacewalk-branding
Obsoletes: rhn-help < 5.3.0
Provides: rhn-help = 5.3.0
Obsoletes: rhn-html < 5.3.0
Provides: rhn-html = 5.3.0
# files html/javascript/{builder.js,controls.js,dragdrop.js,effects.js,
# prototype-1.6.0.js,scriptaculous.js,slider.js,sound.js,unittest.js}
# are licensed under MIT license
License: GPLv2 and MIT

%description -n spacewalk-html
This package contains the HTML files for the Spacewalk web site.


%package -n spacewalk-base
Group: Applications/Internet
Summary: Programs needed to be installed on the RHN Web base classes
Requires: spacewalk-pxt
Provides: spacewalk(spacewalk-base) = %{version}-%{release}
%if 0%{?suse_version}
Requires: perl-RPM2
Requires: perl-Authen-PAM
Requires: perl-Digest-HMAC
Requires: perl-Text-Diff
Requires: perl-DateTime
%endif
Requires: httpd
Obsoletes: rhn-base < 5.3.0
Provides: rhn-base = 5.3.0


%description -n spacewalk-base
This package includes the core RHN:: packages necessary to manipulate
database.  This includes RHN::* and RHN::DB::*.


%package -n spacewalk-base-minimal
Summary: Core of Perl modules for %{name} package
Group: Applications/Internet 
Provides: spacewalk(spacewalk-base-minimal) = %{version}-%{release}
Requires: httpd
Obsoletes: rhn-base-minimal < 5.3.0
Provides: rhn-base-minimal = 5.3.0
Requires: perl-Params-Validate

%description -n spacewalk-base-minimal
Independent Perl modules in the RHN:: name-space.
This are very basic modules need to handle configuration files, database,
sessions and exceptions.

%package -n spacewalk-dobby
Summary: Perl modules and scripts to administer an Oracle database
Group: Applications/Internet
Requires: spacewalk-base
Requires: httpd
Requires: perl-Filesys-Df
Obsoletes: rhn-dobby < 5.3.0
Provides: rhn-dobby = 5.3.0

%description -n spacewalk-dobby
Dobby is collection of Perl modules and scripts to administer an Oracle
database.


%package -n spacewalk-grail
Summary: Grail, a component framework for Spacewalk
Requires: spacewalk-base
Group: Applications/Internet
Obsoletes: rhn-grail < 5.3.0
Provides: rhn-grail = 5.3.0

%description -n spacewalk-grail
A component framework for Spacewalk.


%package -n spacewalk-pxt
Summary: The PXT library for web page templating
Group: Applications/Internet
Requires: spacewalk(spacewalk-base-minimal)
%if 0%{?suse_version}
Requires:  perl-Apache2-Request
Requires:  perl-auditlog-keeper-client
Requires:  perl-BSD-Resource
Requires:  perl-Cache-Cache
Requires:  perl-YAML-Syck
%endif
Requires: httpd
Obsoletes: rhn-pxt < 5.3.0
Provides:  rhn-pxt = 5.3.0

%description -n spacewalk-pxt
This package is the core software of the new Spacewalk site.  It is responsible
for HTML, XML, WML, HDML, and SOAP output of data.  It is more or less
equivalent to things like Apache::ASP and Mason.


%package -n spacewalk-sniglets
Group: Applications/Internet
Summary: PXT Tag handlers
Obsoletes: rhn-sniglets < 5.3.0
Provides:  rhn-sniglets = 5.3.0

%description -n spacewalk-sniglets
This package contains the tag handlers for the PXT templates.


%prep
%setup -q

%build
make -f Makefile.spacewalk-web PERLARGS="INSTALLDIRS=vendor" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make -C modules install DESTDIR=$RPM_BUILD_ROOT PERLARGS="INSTALLDIRS=vendor" %{?_smp_mflags}
make -C html install PREFIX=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name perllocal.pod -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;

mkdir -p $RPM_BUILD_ROOT/%{www_path}/www/htdocs/pub
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/share/rhn/config-defaults
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/init.d
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/cron.daily
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services

install -m 644 conf/rhn_web.conf $RPM_BUILD_ROOT%{_prefix}/share/rhn/config-defaults
install -m 644 conf/rhn_dobby.conf $RPM_BUILD_ROOT%{_prefix}/share/rhn/config-defaults
install -m 755 modules/dobby/scripts/check-database-space-usage.sh $RPM_BUILD_ROOT/%{_sysconfdir}/cron.daily/check-database-space-usage.sh
install -m 0644 etc/sysconfig/SuSEfirewall2.d/services/susemanager-database %{buildroot}/%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/

%post -n spacewalk-pxt
%if 0%{?suse_version}
sysconf_addword /etc/sysconfig/apache2 APACHE_MODULES apreq
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -n spacewalk-base
%defattr(644,root,root,755)
%dir %{perl_vendorlib}/RHN
%dir %{perl_vendorlib}/PXT
%{perl_vendorlib}/RHN.pm
%{perl_vendorlib}/RHN/Access.pm
%{perl_vendorlib}/RHN/Access/
%{perl_vendorlib}/RHN/Action.pm
%{perl_vendorlib}/RHN/Cache/
%{perl_vendorlib}/RHN/Cert.pm
%{perl_vendorlib}/RHN/Channel.pm
%{perl_vendorlib}/RHN/ChannelEditor.pm
%{perl_vendorlib}/RHN/Cleansers.pm
%{perl_vendorlib}/RHN/ConfigChannel.pm
%{perl_vendorlib}/RHN/ConfigRevision.pm
%{perl_vendorlib}/RHN/ContactGroup.pm
%{perl_vendorlib}/RHN/ContactMethod.pm
%{perl_vendorlib}/RHN/CustomInfoKey.pm
%{perl_vendorlib}/RHN/DB/
%{perl_vendorlib}/RHN/DataSource.pm
%{perl_vendorlib}/RHN/DataSource/
%{perl_vendorlib}/RHN/Date.pm
%{perl_vendorlib}/RHN/Entitlements.pm
%{perl_vendorlib}/RHN/Errata.pm
%{perl_vendorlib}/RHN/ErrataEditor.pm
%{perl_vendorlib}/RHN/ErrataTmp.pm
%{perl_vendorlib}/RHN/FileList.pm
%{perl_vendorlib}/RHN/Form.pm
%{perl_vendorlib}/RHN/Form/
%{perl_vendorlib}/RHN/I18N.pm
%{perl_vendorlib}/RHN/KSTree.pm
%{perl_vendorlib}/RHN/Kickstart.pm
%{perl_vendorlib}/RHN/Kickstart/
%{perl_vendorlib}/RHN/Mail.pm
%{perl_vendorlib}/RHN/Manifest.pm
%{perl_vendorlib}/RHN/Org.pm
%{perl_vendorlib}/RHN/Package.pm
%{perl_vendorlib}/RHN/Package/
%{perl_vendorlib}/RHN/Postal.pm
%{perl_vendorlib}/RHN/Profile.pm
%{perl_vendorlib}/RHN/SCDB.pm
%{perl_vendorlib}/RHN/SatCluster.pm
%{perl_vendorlib}/RHN/SatInstall.pm
%{perl_vendorlib}/RHN/SatelliteCert.pm
%{perl_vendorlib}/RHN/Scheduler.pm
%{perl_vendorlib}/RHN/SearchTypes.pm
%{perl_vendorlib}/RHN/Server.pm
%{perl_vendorlib}/RHN/ServerActions.pm
%{perl_vendorlib}/RHN/ServerGroup.pm
%{perl_vendorlib}/RHN/Session.pm
%{perl_vendorlib}/RHN/Set.pm
%{perl_vendorlib}/RHN/SimpleStruct.pm
%{perl_vendorlib}/RHN/StoredMessage.pm
%{perl_vendorlib}/RHN/SystemSnapshot.pm
%{perl_vendorlib}/RHN/TSDB.pm
%{perl_vendorlib}/RHN/Tag.pm
%{perl_vendorlib}/RHN/TemplateString.pm
%{perl_vendorlib}/RHN/TinyURL.pm
%{perl_vendorlib}/RHN/Token.pm
%{perl_vendorlib}/RHN/User.pm
%{perl_vendorlib}/RHN/Utils.pm
%{_mandir}/man3/RHN::ContactGroup.3pm.gz
%{_mandir}/man3/RHN::ContactMethod.3pm.gz
%{_mandir}/man3/RHN::DB::ContactGroup.3pm.gz
%{_mandir}/man3/RHN::DB::ContactMethod.3pm.gz
%{_mandir}/man3/RHN::DB::SatCluster.3pm.gz
%{_mandir}/man3/RHN::DB::ServerGroup.3pm.gz
%{_mandir}/man3/RHN::SCDB.3pm.gz
%{_mandir}/man3/RHN::SatCluster.3pm.gz
%{_mandir}/man3/RHN::Session.3pm.gz
%{_mandir}/man3/RHN::TSDB.3pm.gz

%files -n spacewalk-base-minimal
%defattr(644,root,root,755)
%dir %{perl_vendorlib}/RHN
%dir %{perl_vendorlib}/PXT
%{perl_vendorlib}/RHN/SessionSwap.pm
%{perl_vendorlib}/RHN/Exception.pm
%{perl_vendorlib}/RHN/DB.pm
%{perl_vendorlib}/RHN/DBI.pm
%{perl_vendorlib}/PXT/Config.pm
%attr(640,root,%{apache_group}) %{_prefix}/share/rhn/config-defaults/rhn_web.conf
%dir %{_prefix}/share/rhn
%dir %attr(750,root,%{apache_group}) %{_prefix}/share/rhn/config-defaults
%doc LICENSE

%files -n spacewalk-dobby
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/db-control
%{_mandir}/man1/db-control.1.gz
%{perl_vendorlib}/Dobby.pm
%attr(640,root,%{apache_group}) %{_prefix}/share/rhn/config-defaults/rhn_dobby.conf
%attr(0755,root,root) %{_sysconfdir}/cron.daily/check-database-space-usage.sh
%config %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/susemanager-database
%{perl_vendorlib}/Dobby/
%dir %{_prefix}/share/rhn
%dir %attr(750,root,%{apache_group}) %{_prefix}/share/rhn/config-defaults

%files -n spacewalk-grail
%defattr(644,root,root,755)
%{perl_vendorlib}/Grail.pm
%{perl_vendorlib}/Grail/

%files -n spacewalk-pxt
%defattr(644,root,root,755)
%{perl_vendorlib}/PXT.pm
%{perl_vendorlib}/PXT/
%exclude %{perl_vendorlib}/PXT/Config.pm

%{_mandir}/man3/PXT::ApacheHandler.3pm.gz
%{perl_vendorlib}/PXT.pm
%{perl_vendorlib}/PXT/ACL.pm
%{perl_vendorlib}/PXT/ApacheAuth.pm
%{perl_vendorlib}/PXT/ApacheHandler.pm
%{perl_vendorlib}/PXT/Debug.pm
%{perl_vendorlib}/PXT/HTML.pm
%{perl_vendorlib}/PXT/Handlers.pm
%{perl_vendorlib}/PXT/Parser.pm
%{perl_vendorlib}/PXT/Request.pm
%{perl_vendorlib}/PXT/Trace.pm
%{perl_vendorlib}/PXT/Utils.pm

%files -n spacewalk-sniglets
%defattr(644,root,root,755)
%{perl_vendorlib}/Sniglets.pm
%{perl_vendorlib}/Sniglets/

%files -n spacewalk-html
%defattr(644,root,root,755)
%if !0%{?suse_version}
%dir %{www_path}/www/htdocs
%endif
%{www_path}/www/htdocs/*
%doc LICENSE

# $Id$
%changelog
* Wed Nov 28 2012 Tomas Lestach <tlestach@redhat.com> 1.9.4-1
- 470463 - fixing xmllint issue

* Wed Nov 21 2012 Jan Pazdziora 1.9.3-1
- Revert "removed dead query"
- Revert "The ssm_rollback_by_tag_action_cb method no longer referenced,
  removing."

* Fri Nov 09 2012 Jan Pazdziora 1.9.2-1
- 490524 - Return the datetime in the local time zone.
- 490524 - Epoch is always in UTC, no time_zone setting for epoch case.
- Function date_to_epoch made obsolete, not used anymore.
- The from_zone parameter is not used anywhere.
- Use RHN::Date where it is used (only).
- 490524 - Avoid initializing the object with local only to call time_zone
  right away.
- 490524 - Shortcut RHN::Date->now->long_date, avoiding DateTime.

* Wed Oct 31 2012 Jan Pazdziora 1.9.1-1
- Bumping version string to 1.9.
- Bumping package versions for 1.9.

* Tue Oct 30 2012 Jan Pazdziora 1.8.48-1
- Update the copyright year.
- Make RHN::DB::SystemSnapshot usable with strict.

* Mon Oct 22 2012 Jan Pazdziora 1.8.47-1
- 852039 - get rid of useless error messages when verifying backup with db-
  control
- 552628 - added reset-password to man page
- 552628 - alter command can't use bind variables
- 852038 - Using fetchall_arrayref instead of fullfetch_arrayref.
- 850714 - do not push strings into an array, when array is expected

* Mon Oct 22 2012 Jan Pazdziora 1.8.46-1
- removing spurious debugging line from check-database-space-usage.sh
- do not restore dirs if there is none to restore
- ignore missing backup_dir on old dumps
- 825804 - check-oracle-space-usage.sh renamed to check-database-space-usage.sh
- 815236 - use df with POSIX compatibility

* Mon Oct 22 2012 Miroslav Suchý
- 805822 - warn about parsing backup log
- 805822 - mark some commands as Oracle only and sync --help with man page
- 815236 - adopt check-oracle-space-usage.sh for PotgreSQL

* Mon Oct 22 2012 Miroslav Suchý
- 805822 - reword --help page

* Mon Oct 22 2012 Miroslav Suchý
- drop plpgsql language before restore
- implement on-line backup and restore on PG
- 805822 - edit man page to include PostgreSQL specific commands
- 663315 - wait until database is really offline
- log into control file empty directories
- correctly set ownership of restored files
- set ownership of restored files under PG
- restore selinux context after restore
- implement "db-control restore" on PG
- db-control under PG can be run as root or postgres user
- implement "db-control examine/verify" on PG
- put into control file base directory
- if size is undef write 0
- implement "db-control backup" on PG
- implement "db-control reset-password" on PG
- implement "db-control report-stats" on PG
- unify connect() with RHN::DBI
- implement "db-control gather-stats" under PG
- mark "db-control extend" and "db-control shrink-segments" as Oracle only
- implement "db-control tablesizes" under PG
- implement "db-control report" under PG
- mark set-optimizer and get-optimizer as Oracle only
- implement "db-control start" and "db-control stop" under PG
- implement "db-control status" under PG

* Tue Oct 16 2012 Jan Pazdziora 1.8.42-1
- Adding use which seems to be needed.

* Fri Oct 12 2012 Jan Pazdziora 1.8.41-1
- 844433 - fix cloning a child channel with a parent in different org
- Bind bytea with PG_BYTEA.

* Thu Oct 11 2012 Jan Pazdziora 1.8.40-1
- Dead code removal.

* Thu Oct 11 2012 Michael Mraka <michael.mraka@redhat.com> 1.8.39-1
- 847194 - Document & set default web.smtp_server
- Module Sniglets::ListView::TracerList not used, removing.
- The database_queries.xml do not seem to be used, removing.

* Thu Oct 11 2012 Tomas Lestach <tlestach@redhat.com> 1.8.38-1
- reverting of web.chat_enabled -> java.chat_enabled translation
- Removing use which is not used.
- Methods server_group_count no longer referenced, removing.
- Methods lookup_key were deprecated long enough, removing.
- Methods compatible_with_server no longer referenced, removing.
- The org_default method no longer referenced, removing.
- Methods package_groups no longer referenced, removing.
- The has_virtualization_entitlement method no longer referenced, removing.
- ACL handler system_entitled no longer used, removing.
- ACL handler system_has_virtualization_entitlement no longer used, removing.
- The latest_packages_in_channel_tree method no longer referenced, removing.
- The /network/systems/details/kickstart/* is not used for a long time.

* Wed Oct 10 2012 Jan Pazdziora 1.8.37-1
- Dead code removal.
- RHN Proxies older than version 5 as no longer supported.

* Thu Sep 20 2012 Jan Pazdziora 1.8.36-1
- Avoid link without eid parameter filled.

* Fri Sep 07 2012 Tomas Lestach <tlestach@redhat.com> 1.8.35-1
- restore changelog
- changing web.chat_enabled -> java.chat_enabled
- move java related configuration the rhn_java.conf

* Wed Sep 05 2012 Stephen Herr <sherr@redhat.com> 1.8.34-1
- 815964 - moving monitoring probe batch option from rhn.conf to rhn_web.conf

* Fri Aug 31 2012 Jan Pazdziora 1.8.33-1
- 852048 - fix typo in db-control man page

* Tue Aug 07 2012 Jan Pazdziora 1.8.32-1
- Remove hints that should no longer be needed.

* Wed Aug 01 2012 Jan Pazdziora 1.8.31-1
- fix outer join syntax

* Mon Jul 30 2012 Tomas Lestach <tlestach@redhat.com> 1.8.30-1
- remove usage of org_applicant user role
- remove usage of rhn_support user role
- remove usage of rhn_superuser user role

* Fri Jul 20 2012 Tomas Kasparek <tkasparek@redhat.com> 1.8.29-1
- 841453  - forcing parameter to be numeric
- Forcing parameter to be string

* Fri Jul 13 2012 Jan Pazdziora 1.8.28-1
- OpenSCAP Integration -- XCCDF Scan Diff

* Thu Jul 12 2012 Michael Mraka <michael.mraka@redhat.com> 1.8.27-1
- Fix ISE on pgsql: Error message: RHN::Exception: DBD::Pg::st execute failed

* Tue Jul 10 2012 Michael Mraka <michael.mraka@redhat.com> 1.8.26-1
- cross-database references are not implemented: pe.evr.as_vre_simple

* Thu Jun 28 2012 Michael Mraka <michael.mraka@redhat.com> 1.8.25-1
- removed unused query

* Wed Jun 27 2012 Michael Mraka <michael.mraka@redhat.com> 1.8.24-1
- ORDER BY expressions must appear in select list
- removed dead query
- fixed ssm provisioning

* Wed Jun 27 2012 Jan Pazdziora 1.8.23-1
- The remove_virtualization_host_entitlement no longer used, removing.
- The rhn:delete_server_cb and delete_server_cb no longer used, removing.
- The delete_confirm.pxt was replaced by DeleteConfirm.do.

* Wed Jun 27 2012 Jan Pazdziora 1.8.22-1
- Perl Notes pages seem like dead code.

* Wed Jun 27 2012 Michael Mraka <michael.mraka@redhat.com> 1.8.21-1
- 835608 - error messages in PostgreSQL have different pattern

* Tue Jun 26 2012 Michael Mraka <michael.mraka@redhat.com> 1.8.20-1
- Correcting ISE on postgresql: NVL keyword

* Fri Jun 22 2012 Jan Pazdziora 1.8.19-1
- For the localhost:5432 case, use the Unix socket local connection.

* Fri Jun 08 2012 Jan Pazdziora 1.8.18-1
- 803370 - call to rhn_server.tag_delete db agnostic

* Mon Jun 04 2012 Miroslav Suchý <msuchy@redhat.com> 1.8.17-1
- Add support for studio image deployments (web UI) (jrenner@suse.de)

* Thu May 31 2012 Jan Pazdziora 1.8.16-1
- OpenSCAP integration -- A simple search page.

* Fri May 25 2012 Stephen Herr <sherr@redhat.com> 1.8.15-1
- 824879, 825279 - Sometimes the return_link on the SSM Clear button does not
  work

* Thu May 10 2012 Jan Pazdziora 1.8.14-1
- Split OpenSCAP and AuditReviewing up (slukasik@redhat.com)

* Thu Apr 26 2012 Miroslav Suchý <msuchy@redhat.com> 1.8.13-1
- add AS syntax for PostgreSQL

* Mon Apr 23 2012 Miroslav Suchý <msuchy@redhat.com> 1.8.12-1
- Fix errata clone name generation in perl code

* Thu Apr 19 2012 Jan Pazdziora 1.8.11-1
- Removed double-dash from copyright notice on error pages.

* Tue Apr 17 2012 Jan Pazdziora 1.8.10-1
- Broken link patch submitted on behalf of Michael Calmer (sherr@redhat.com)

* Thu Apr 12 2012 Stephen Herr <sherr@redhat.com> 1.8.9-1
- 812031 - Update perl channel-select-dropdowns to use the same hierarchical
  sort as java pages (sherr@redhat.com)

* Thu Apr 05 2012 Jan Pazdziora 1.8.8-1
- Fix naming of cloned errata to replace only the first 2 chars
  (tlestach@redhat.com)

* Tue Apr 03 2012 Jan Pazdziora 1.8.7-1
- 806439 - Changing perl sitenav too (sherr@redhat.com)

* Wed Mar 21 2012 Jan Pazdziora 1.8.6-1
- Fixing regular_systems_in_channel_family for PostgreSQL.

* Tue Mar 20 2012 Michael Mraka <michael.mraka@redhat.com> 1.8.5-1
- fixed rhn_server.delete_from_servergroup() call
- Show details of SCAP event.

* Mon Mar 19 2012 Jan Pazdziora 1.8.4-1
- We no longer have /install/index.pxt, so satellite_install cannot be used.

* Tue Mar 13 2012 Simon Lukasik <slukasik@redhat.com> 1.8.3-1
- OpenSCAP integration  -- Show results for system on web.
  (slukasik@redhat.com)

* Tue Mar 13 2012 Jan Pazdziora 1.8.2-1
- Need to point to ReleventErrata.do from .pxt pages as well.
- PXT::Request->clear_session is not used anywhere, thus removing
  (mzazrivec@redhat.com)

* Fri Mar 02 2012 Jan Pazdziora 1.8.1-1
- Bumping version string to 1.8.

* Fri Mar 02 2012 Jan Pazdziora 1.7.27-1
- Update the copyright year info.

* Thu Mar 01 2012 Miroslav Suchý 1.7.26-1
- call plsql function or procedure correctly

* Mon Feb 27 2012 Jan Pazdziora 1.7.25-1
- call composite type correctly on Pg (msuchy@redhat.com)
- call procedure compatible way (Pg) (msuchy@redhat.com)

* Wed Feb 22 2012 Miroslav Suchý 1.7.24-1
- automatically focus search form (msuchy@redhat.com)

* Mon Feb 20 2012 Jan Pazdziora 1.7.23-1
- Removing rhnUser synonym and just using the base web_contact.
- Methods users_in_org and users_in_org_overview do not seem to be used,
  removing.
- The valid_cert_countries in RHN::DB::SatInstall is not used, spacewalk-setup
  has its own version.

* Mon Feb 20 2012 Miroslav Suchý 1.7.22-1
- call procedure compatible way (Pg) (msuchy@redhat.com)
- check if error is RHN::Exception (msuchy@redhat.com)

* Mon Feb 20 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.21-1
- fixed list of patches in solaris package

* Thu Feb 16 2012 Jan Pazdziora 1.7.20-1
- The iso_path parameter is not used anywere, removing the verify_file_access
  cleanser.

* Thu Feb 16 2012 Jan Pazdziora 1.7.19-1
- With update_errata_cache removed, update_cache_for_server is not called
  either, removing.
- With log_user_in removed, removing mark_log_in as well.
- With log_user_in removed, removing clear_selections as well.
- With validate_password_pam gone, Authen::PAM and pam_conversation_func are no
  longer called.
- With check_login gone, validate_password (and validate_password_pam) are not
  longer used.
- With validate_cert gone and no longer calling str2time, use Date::Parse is
  not needed.
- Method has_incomplete_info no longer used, removing.
- With rhn_login_cb gone, update_errata_cache is not longer used.
- With rhn_login_cb gone, log_user_in is not longer used.
- The check_login no longer invoked, removing.
- With the if test for validate_cert gone, /errors/cert-expired.pxt is no
  longer used.
- The validate_cert is no longer called, removing.
- The clear_user method no longer invoked, removing.
- We no longer check cookie_test.
- With rhn_login_cb gone, /errors/cookies.pxt is no longer used, removing.
- The rhn:login_cb and rhn_login_cb are no longer used, removing.
- The [login_form_hidden] is not longer used, removing.
- login_form.pxi no longer used, removing.
- In the /errors/permission.pxt, redirect to the main page to log in again.
- The $package_name_ids parameter never passed.

* Wed Feb 15 2012 Jan Pazdziora 1.7.18-1
- The note_count value is nowhere used in the application code, removing from
  selects.

* Mon Feb 13 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.17-1
- PostgreSQL: Fix adding systems to a system group

* Tue Feb 07 2012 Jan Pazdziora 1.7.16-1
- Updating the oversight in license texts.

* Tue Feb 07 2012 Jan Pazdziora 1.7.15-1
- remove unused code (mzazrivec@redhat.com)
- pgsql: fix notification method deletion (mzazrivec@redhat.com)
- pgsql: fix notification method creation (mzazrivec@redhat.com)

* Wed Feb 01 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.14-1
- fixing string quoting

* Tue Jan 31 2012 Miroslav Suchý 1.7.13-1
- port usage of sequences to PostgreSQL

* Tue Jan 31 2012 Jan Pazdziora 1.7.12-1
- code cleanup: users are not created in web any more (msuchy@redhat.com)
- The RHN::DB::connect does not accept any arguments anymore.
- Factor the connection parameters config read to RHN::DBI, start to use it in
  RHN::DB, also support just one database connection.
- Removing code which is long commented out.
- Removing the web.debug_disable_database option -- it is not supported beyond
  RHN::DB anyway.

* Mon Jan 30 2012 Jan Pazdziora 1.7.11-1
- One sequence_nextval fix.
- Refactored the evr_t(null, ...) and null and max.
- The $rhn_class is always empty, removing.

* Mon Jan 30 2012 Miroslav Suchý 1.7.10-1
- In Spacewalk do not test presence of rhn-proxy family, if we want to display
  list of Proxies
- The target_systems.pxt was migrated to Java years ago.

* Thu Jan 26 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.9-1
- delete server sets at once

* Wed Jan 25 2012 Jan Pazdziora 1.7.8-1
- For DBD::Pg, just use its builtin ping, instead of doing SELECT.
- Make it easier to subclass RHN::DB, use the $class which was passed in.

* Mon Jan 23 2012 Jan Pazdziora 1.7.7-1
- 783223 - fixing sysdate issue in rhn-enable-monitoring.pl.
- Show Proxy tabs on Spacewalk (msuchy@redhat.com)

* Fri Jan 13 2012 Tomas Lestach <tlestach@redhat.com> 1.7.6-1
- 773605 - bring back deleted system_list from the other side of Styx river
  (tlestach@redhat.com)
- 515653 - unify channel architecture label (mzazrivec@redhat.com)

* Wed Jan 04 2012 Tomas Lestach <tlestach@redhat.com> 1.7.5-1
- 771634 - remove semi-colon at the end of queries (tlestach@redhat.com)

* Tue Jan 03 2012 Jan Pazdziora 1.7.4-1
- The RHN::Form::Widget::Multiple, RHN::Form::Widget::Password, and
  RHN::Form::Widget::Spacer seem not used, removing.
- After removal of RHN::CryptoKey, RHN::DB::CryptoKey is no longer used,
  removing.
- After removal of RHN::AppInstall::Parser, RHN::Form::Parser is no longer
  used, removing.
- After removal of RHN::ProxyInstall, RHN::CryptoKey is no longer used,
  removing.

* Mon Jan 02 2012 Michael Mraka <michael.mraka@redhat.com> 1.7.3-1
- fixed merging channels

* Mon Jan 02 2012 Tomas Lestach <tlestach@redhat.com> 1.7.2-1
- 771214 - add missing widget require (tlestach@redhat.com)

* Thu Dec 22 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.7.1-1
- web.version: 1.7 nightly

* Wed Dec 21 2011 Milan Zazrivec <mzazrivec@redhat.com> 1.6.36-1
- update copyright info

* Mon Dec 12 2011 Tomas Lestach <tlestach@redhat.com> 1.6.35-1
- add missing requires (tlestach@redhat.com)
- fix 500 Error - ISE on network/systems/ssm/provisioning/remote_command.pxt
  (tlestach@redhat.com)

* Mon Dec 12 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.34-1
- fix Package queries
- fix ORDER BY expression in DISTINCT select
- use real table name rhn_check_probe
- replace (+) with ANSI left join (PG)
- set selinux_ctx to undef if it is empty
- No need to convert numeric values to upper.
- convert decode to case

* Wed Dec 07 2011 Miroslav Suchý 1.6.33-1
- code cleanup
- do not allow to configure or activate proxy from WebUI

* Tue Dec 06 2011 Jan Pazdziora 1.6.32-1
- IPv6: reprovisioning with static network interface (mzazrivec@redhat.com)
- code cleanup - function base_entitlement is not used anymore
  (msuchy@redhat.com)
- code cleanup - function addon_entitlements is not used anymore
  (msuchy@redhat.com)
- code cleanup - function ks_session_redir is not used anymore
  (msuchy@redhat.com)
- code cleanup - callback rhn:delete_servers_cb is not used anymore
  (msuchy@redhat.com)
- code cleanup - callback server_hardware_list_refresh_cb is not used anymore
  (msuchy@redhat.com)
- code cleanup - tag rhn-server-network-details is not used anymore
  (msuchy@redhat.com)
- code cleanup - tag rhn-server-device is not used anymore (msuchy@redhat.com)
- code cleanup - tag rhn-dmi-info is not used anymore (msuchy@redhat.com)
- code cleanup - tag rhn-server-hardware-profile is not used anywhere
  (msuchy@redhat.com)

* Tue Nov 29 2011 Miroslav Suchý 1.6.31-1
- IPv6: code cleanup - package RHN::DB::Server::NetInterface is not used
  anymore
- IPv6: code cleanup - function get_net_interfaces is not used anymore
- IPv6: code cleanup - function server_network_interfaces is not used anymore
- IPv6: code cleanup - tag rhn-server-network-interfaces is not used anywhere

* Fri Nov 25 2011 Jan Pazdziora 1.6.30-1
- Replace nvl with coalesce.
- Matching the to_char prototype.
- Matching the varchar column to varchar literal.
- Replace decode with case when.
- Replace sysdate with current_timestamp.

* Wed Nov 23 2011 Jan Pazdziora 1.6.29-1
- Fixing cancel a scheduled action on a server.

* Wed Nov 16 2011 Tomas Lestach <tlestach@redhat.com> 1.6.28-1
- 754379 - fix deletion-url in pxt pages (tlestach@redhat.com)

* Fri Nov 04 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.27-1
- removed aliases from SET part of UPDATE

* Wed Nov 02 2011 Jan Pazdziora 1.6.26-1
- Workaround for DBD::Pg bug https://rt.cpan.org/Ticket/Display.html?id=70953.

* Fri Sep 30 2011 Jan Pazdziora 1.6.25-1
- 678118 - if system already is proxy, losen the ACL and show the tab.
- Recent commit makes version_string_to_evr_array unused, dropping.
- Removing proxy_evr_at_least, org_proxy_evr_at_least, aclOrgProxyEvrAtLeast as
  they are no longer used.
- Remove proxy_evr_at_least ACLs -- all supported proxy versions are 3+.
- Make the pxt Connection acl match the java version -- new acl
  org_has_proxies.

* Fri Sep 30 2011 Jan Pazdziora 1.6.24-1
- 621531 - update web Config to use the new /usr/share/rhn/config-defaults
  location.
- 621531 - move /etc/rhn/default to /usr/share/rhn/config-defaults (web).

* Fri Sep 23 2011 Jan Pazdziora 1.6.23-1
- The /etc/rhn/default/rhn_web.conf does not need to be provided by -pxt since
  it is provided by -base-minimal.

* Mon Sep 19 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.22-1
- 723461 - let emails be sent to localhost by default

* Fri Sep 16 2011 Jan Pazdziora 1.6.21-1
- CVE-2011-3344, 731647 - HTML-encode the self-referencing link.

* Thu Sep 15 2011 Jan Pazdziora 1.6.20-1
- Revert "529483 - adding referer check to perl stack"

* Fri Sep 09 2011 Jan Pazdziora 1.6.19-1
- 616175 - observe the port specified in the URL even for https.

* Thu Aug 25 2011 Miroslav Suchý 1.6.18-1
- 705363 - spacewalk-base and spacewalk-base-minimal are now disjunctive
  remove the provide from spacewalk-base

* Wed Aug 24 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.17-1
- fixed typo in sql query

* Tue Aug 23 2011 Miroslav Suchý 1.6.16-1
- 705363 - reformat description text for spacewalk-base-minimal not to exceed
  80 columns
- 705363 - do not provide perl(PXT::Config) by two packages

* Mon Aug 22 2011 Martin Minar <mminar@redhat.com> 1.6.15-1
- 585010 - mark the Update List button with it so that we can disable it later.
  (jpazdziora@redhat.com)

* Fri Aug 19 2011 Miroslav Suchý 1.6.14-1
- 705363 - remove executable bit from modules and javascript
- 705363 - Replace word "config" with "configuration" in spacewalk-base-minimal
  description
- 705363 - normalize home page URL

* Fri Aug 12 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.13-1
- removed unnecessary join

* Thu Aug 11 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.12-1
- fixed couple more joins
- removed typo parenthesis

* Wed Aug 10 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.11-1
- COALESCE works in both db backends

* Wed Aug 10 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.10-1
- replace oracle specific syntax with ANSI one
- made NVL2 work in both db backends

* Mon Aug 08 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.9-1
- fixed re-activation key in PostgreSQL

* Thu Aug 04 2011 Aron Parsons <aparsons@redhat.com> 1.6.8-1
- add support for custom messages in the header, footer and login pages
  (aparsons@redhat.com)

* Fri Jul 29 2011 Miroslav Suchý 1.6.7-1
- Revert "adding tomcat require to spacewalk-base-minimal"

* Fri Jul 29 2011 Miroslav Suchý 1.6.6-1
- 705363 - remove obscure keys forgotten for ages
- 705363 - Escape percentage symbol in changelog
- 705363 - include LICENSE file in spacewalk-html
- 705363 - defattr is not required any more if do not differ from default
- 705363 - add _smp_mflags macro to make to utilize all CPUs while building
- 705363 - require Perl for all subpackages with Perl modules
- code cleanup - Proxy 4.x and older are not supported for some time, removing
- 705363 - description must end with full stop
- 705363 - spacewalk-web package summary contains lower-case `rpm'
  abbreviation. Use upper case.
- 705363 - clarify description and summary
- 705363 - be more specific about license
- 705363 - change summary of package

* Fri Jul 29 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.5-1
- 724963 - use ANSI joins
- 724963 - use LEFT JOIN instead of MINUS

* Wed Jul 27 2011 Michael Mraka <michael.mraka@redhat.com> 1.6.4-1
- fixed ORA-00904 in remote commands

* Fri Jul 22 2011 Jan Pazdziora 1.6.3-1
- We only support version 14 and newer of Fedora, removing conditions for old
  versions.

* Thu Jul 21 2011 Miroslav Suchý 1.6.2-1
- Sysdate replaced with current_timestamp

* Wed Jul 20 2011 Jan Pazdziora 1.6.1-1
- Bumping up the Spacewalk version to 1.6 (shown on the WebUI).

* Tue Jul 19 2011 Jan Pazdziora 1.5.16-1
- Updating the copyright years.

* Mon Jul 11 2011 Jan Pazdziora 1.5.15-1
- Refactor RedHat.do to Vendor.do (jrenner@suse.de)

* Mon May 30 2011 Michael Mraka <michael.mraka@redhat.com> 1.5.14-1
- made some queries PG compatible
- fixing ISE in errata cloning

* Tue May 24 2011 Jan Pazdziora 1.5.13-1
- replaced (+) with ANSI left join (je@rockenstein.de)

* Thu May 19 2011 Michael Mraka <michael.mraka@redhat.com> 1.5.12-1
- made queries PostgreSQL compatible

* Tue May 17 2011 Miroslav Suchý 1.5.11-1
- spacewalk-pxt.noarch: W: spelling-error %%description -l en_US equlivalent ->
  equivalent, equivalence, univalent (msuchy@redhat.com)

* Tue May 17 2011 Miroslav Suchý 1.5.10-1
- add GPLv2 LICENSE
- migrate .htaccess files to apache core configuration

* Mon May 16 2011 Miroslav Suchý 1.5.9-1
- cleanup - removing old files, and unused sections in .htaccess

* Tue May 10 2011 Jan Pazdziora 1.5.8-1
- Fix remote command schedule date on postgresql (Ville.Salmela@csc.fi)

* Fri May 06 2011 Jan Pazdziora 1.5.7-1
- Fix remote commands on Spacewalk 1.4 and PostgreSQL (Ville.Salmela@csc.fi)

* Thu May 05 2011 Miroslav Suchý 1.5.6-1
- 682112 - correct column name (mzazrivec@redhat.com)
- 682112 - correct displayed systems consuming channel entitlements
  (mzazrivec@redhat.com)

* Mon May 02 2011 Jan Pazdziora 1.5.5-1
- Fixing set_err invocation to match the prototype.

* Mon May 02 2011 Jan Pazdziora 1.5.4-1
- Patch to run remote commands on multiple machines on Spacewalk 1.4
  PostgreSQL. (Ville.Salmela@csc.fi)
- Removal of system_value_edit makes set_custom_value unused, dropping.
- Removal of remove_system_value makes remove_custom_value unused, dropping.
- The can_delete_custominfokey no longer used after previous removals,
  removing.

* Fri Apr 29 2011 Tomas Lestach <tlestach@redhat.com> 1.5.3-1
- fixing system query systems_with_package (tlestach@redhat.com)
- remove macro from changelog (msuchy@redhat.com)

* Fri Apr 15 2011 Jan Pazdziora 1.5.2-1
- show weak deps in Web UI (mc@suse.de)
- 674806 - get / set oracle db optimizer (mzazrivec@redhat.com)

* Mon Apr 11 2011 Miroslav Suchý 1.5.1-1
- bump up version of Spacewalk - both in webUI and API version
- Bumping package versions for 1.5

* Fri Apr 08 2011 Jan Pazdziora 1.4.20-1
- use new database columns errata_from and bug url also in the perl code
  (mc@suse.de)

* Fri Apr 08 2011 Jan Pazdziora 1.4.19-1
- Putting back use RHN::Exception (with explicit import of throw).

* Fri Apr 08 2011 Miroslav Suchý 1.4.18-1
- update copyright years (msuchy@redhat.com)

* Thu Apr 07 2011 Jan Pazdziora 1.4.17-1
- replace (+) with ANSI left join (PG) (michael.mraka@redhat.com)
- Removing .pxt and methods since custominfo were migrated to Java by now.
- Cleanup of use in Perl modules.
- Removing .pxt and methods after all activation key pages were migrated
  to Java by now.

* Tue Apr 05 2011 Jan Pazdziora 1.4.16-1
- Fixing PostgreSQL distinct/order by issue in
  tags_for_provisioning_entitled_in_set.

* Thu Mar 24 2011 Jan Pazdziora 1.4.15-1
- Fixing previous taggable_systems_in_set fix (Oracle, this time).
- update copyright years (msuchy@redhat.com)
- implement common access keys (msuchy@redhat.com)

* Thu Mar 24 2011 Jan Pazdziora 1.4.14-1
- As PostgreSQL does not support table aliases in updates, remove them.

* Tue Mar 22 2011 Jan Pazdziora 1.4.13-1
- Moving the Requires: httpd from sniglets to base-minimal, dobby, and pxt
  which actually have %%files with apache group in them.
- No need to require mod_perl explicitly in spacewalk-sniglets, we will get it
  via perl(Apache2::Cookie) and perl-libapreq2 from spacewalk-pxt.
- Removing RHEL 4 specific Requires as we no longer support Spacewalk on RHEL 4.
- Fixing taggable_systems_in_set PostgreSQL issues.
- Fixing custom_info_keys PostgreSQL issue.
- Fixing the system_set_supports_reboot PostgreSQL issue.

* Tue Mar 22 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.12-1
- evaluate default_connection in runtime not in use RHN::DB time

* Fri Mar 18 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.11-1
- fixed package_removal_failures in postgresql

* Wed Mar 16 2011 Miroslav Suchý <msuchy@redhat.com> 1.4.10-1
- made /network/systems/details/history/event.pxt work on postgresql
- Fixing is_eoled, replacing sysdate with current_timestamp.

* Wed Mar 09 2011 Jan Pazdziora 1.4.9-1
- Fixing system group operations (PostgreSQL).
- Using sequence_nextval instead of .nextval.

* Wed Mar 02 2011 Tomas Lestach <tlestach@redhat.com> 1.4.8-1
- consider also package arch when searching systems accorging to a package
  (tlestach@redhat.com)
- Removal of rhn-load-config.pl made
  RHN::DB::SatInstall::get_nls_database_parameters unused, removing.
  (jpazdziora@redhat.com)
- Removal of rhn-load-config.pl made RHN::SatInstall::generate_secret unused,
  removing. (jpazdziora@redhat.com)

* Mon Feb 28 2011 Jan Pazdziora 1.4.7-1
- Replacing date arithmetics with current_timestamp + numtodsinterval().
- We need to use current_timestamp instead of sysdate.
- Use sequence_nextval function.
- PostgreSQL does not like table alias on insert.
- We need to use global evr_t_as_vre_simple instead of PE.evr.as_vre_simple().
- The use of verify_channel_role is always in scalar context, no need to user
  the user_role_check_debug.
- Prevent empty strings from being inserted to the database.
- Adding the AS keyword to column aliases for PostgreSQL.

* Fri Feb 25 2011 Jan Pazdziora 1.4.6-1
- 680375 - we do not want the locked status (icon) to hide the the other
  statuses, we add separate padlock icon.
- Fixing systems_in_channel_family query for PostgreSQL.
- The /network/systems/details/hardware.pxt was replaced by
  /rhn/systems/details/SystemHardware.do.

* Thu Feb 24 2011 Jan Pazdziora 1.4.5-1
- The module Text::Diff is no longer needed, removing its use.

* Fri Feb 18 2011 Jan Pazdziora 1.4.4-1
- Localize the filehandle globs; also use three-parameter opens.

* Wed Feb 16 2011 Miroslav Suchý <msuchy@redhat.com> 1.4.3-1
- enable RHN Proxy 5.4 on RHEL6 (msuchy@redhat.com)
- server_event_config_deploy just called server_event_config_revisions without
  adding any value, removing. (jpazdziora@redhat.com)

* Wed Feb 09 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.2-1
- 552628 - implemented db-control reset-password
- removed remote_dsn - it's always empty
- 552628 - use database credentials from rhn.conf
- The RHN::Utils::parametrize is not used anywhere, removing.

* Wed Feb 02 2011 Tomas Lestach <tlestach@redhat.com> 1.4.1-1
- bumping web.version to 1.4 nightly (tlestach@redhat.com)
- Bumping package versions for 1.4 (tlestach@redhat.com)

* Wed Feb 02 2011 Tomas Lestach <tlestach@redhat.com> 1.3.24-1
- removing nightly from web.version (tlestach@redhat.com)

* Thu Jan 20 2011 Tomas Lestach <tlestach@redhat.com> 1.3.23-1
- updating Copyright years for year 2011 (tlestach@redhat.com)
- Removing RHN::DB::SatInstall::clear_db, it was last referenced by rhn-
  populate-database.pl. (jpazdziora@redhat.com)

* Wed Jan 19 2011 Tomas Lestach <tlestach@redhat.com> 1.3.22-1
- extending OS check expression (tlestach@redhat.com)

* Wed Jan 19 2011 Tomas Lestach <tlestach@redhat.com> 1.3.21-1
- adding tomcat require to spacewalk-base-minimal (tlestach@redhat.com)
- 670185 - rephrasing the status information to be more clear
  (tlestach@redhat.com)

* Mon Jan 03 2011 Jan Pazdziora 1.3.20-1
- token_channel_select.js not referenced, removing.
- As RHN::DB::Search is gone, system_search_setbuilder.xml is not used,
  removing.
- subscribe_confirm.pxt not referenced, removing.
- The RHL9 and RHEL 3 release notes are not referenced, removing.
- countdown.js does not seem to be used, removing.
- Since RHN::DataSource::ContactGroup is gone, contact_group_queries.xml is
  unused, removing.
- PXT::Debug::log_dump not used anywhere, removing.
- RHN::Access::User not used anywhere, removing.

* Thu Dec 23 2010 Aron Parsons <aparsons@redhat.com> 1.3.19-1
- remove symlink that accidentily got added (aparsons@redhat.com)

* Thu Dec 23 2010 Aron Parsons <aparsons@redhat.com> 1.3.18-1
- bump API version number for recent API changes (aparsons@redhat.com)

* Thu Dec 23 2010 Jan Pazdziora 1.3.17-1
- Since ssm_channel_change_conf is gone, ssm_channel_change_conf_provider is
  not used anymore, removing.
- Package RHN::Access::Errata not used, removing.
- RHN::UserActions not used anywhere, removing.

* Tue Dec 21 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.16-1
- 664487 - fixed space report query
- fixed prototype-*.js reference

* Fri Dec 17 2010 Jan Pazdziora 1.3.15-1
- 656963 - the script has to start with #!/bin/sh.
- 656963 - move "Generate jabberd config file" script to correct activity
  (msuchy@redhat.com)
- 663304 - we do not put alias in INSERTs since commit b950aa91
  (msuchy@redhat.com)

* Wed Dec 15 2010 Miroslav Suchý <msuchy@redhat.com> 1.3.14-1
- 663304 - we do not put alias in INSERTs since commit b950aa91
- 656963 - wrap up run-script using activity

* Tue Dec 14 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.13-1
- fixed undefined variable

* Mon Dec 13 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.12-1
- 517455 - adding tablesizes to SYNOPSIS section of db-control man page.
- 617305 - exit value 0 is returned by all db-control commands by default.
- removed unused overview query
- 656963 - create jabberd config via spacewalk-setup-jabberd

* Tue Dec 07 2010 Lukas Zapletal 1.3.11-1
- 642988 - ISE when setting Software Channel Entitlements

* Thu Dec 02 2010 Lukas Zapletal 1.3.10-1
- 658256 - Error 500 - ISE - when scheduling remote commands (proper fix)

* Wed Dec 01 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.9-1
- Reverted "658256 - Error 500 - ISE - when scheduling remote commands"

* Wed Dec 01 2010 Lukas Zapletal 1.3.8-1
- 658256 - Error 500 - ISE - when scheduling remote commands

* Sat Nov 27 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.7-1
- 649706 - execute all recomendations from segment advisor

* Fri Nov 26 2010 Jan Pazdziora 1.3.6-1
- Fix handling of eval (DBD::Oracle).
- 642285 - introducing disabled TaskStatus page (tlestach@redhat.com)

* Tue Nov 23 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.5-1
- fixed Notification Methods (PG)

* Mon Nov 22 2010 Lukas Zapletal 1.3.4-1
- Adding missing monitoring state (UNKNOWN)

* Fri Nov 19 2010 Lukas Zapletal 1.3.3-1
- Removing from SQL clause (System_queries) causing bugs in monitoring

* Fri Nov 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.2-1
- fixed outer joins

* Thu Nov 18 2010 Lukas Zapletal 1.3.1-1
- Replacing DECODE function with CASE-SWITCH (4x)
- Marking the master as nightly. 
- Bumping package versions for 1.3. 

* Mon Nov 15 2010 Jan Pazdziora 1.2.27-1
- bumping api version (jsherril@redhat.com)

* Thu Nov 11 2010 Jan Pazdziora 1.2.26-1
- make event.pxt work with both Oracle and PostgreSQL (mzazrivec@redhat.com)
- use ansi syntax in outer join (mzazrivec@redhat.com)

* Thu Nov 11 2010 Jan Pazdziora 1.2.25-1
- Bumping up version to 1.2.

* Wed Nov 10 2010 Lukas Zapletal 1.2.24-1
- Fixing table aliases for DISTINCT queries (PG)

* Wed Nov 10 2010 Jan Pazdziora 1.2.23-1
- use ansi syntax in outer join (mzazrivec@redhat.com)
- fixing queries, where rhnServer was unexpectedly joined to the query
  (tlestach@redhat.com)

* Wed Nov 03 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.22-1
- 647099 - add API call isMonitoringEnabledBySystemId (msuchy@redhat.com)
- migrating change log to java, and making it use the rpm itself instead of the
  database (jsherril@redhat.com)

* Tue Nov 02 2010 Jan Pazdziora 1.2.21-1
- Update copyright years in web/.
- bumping API version to identify new API call availability
  (tlestach@redhat.com)
- Fixing table name aliases (PE -> SPE) (lzap+git@redhat.com)

* Mon Nov 01 2010 Jan Pazdziora 1.2.20-1
- The sequence_nextval method returns sequence value both on Oracle and
  PostgreSQL.
- Only do Oracle LOB handling for Oracle database backend.
- The sequence_nextval method returns sequence value both on Oracle and
  PostgreSQL.
- Use ANSI syntax for outer join.
- 612581 - change egrep to grep -E (msuchy@redhat.com)

* Fri Oct 29 2010 Jan Pazdziora 1.2.19-1
- Making DISTINCT-ORDER BY package/system queries portable
  (lzap+git@redhat.com)
- Simplifying ORDER BY clauses in package queries (lzap+git@redhat.com)
- Revert "Reverting "Removed unnecessary ORDER BY" commits and fixing"
  (lzap+git@redhat.com)

* Fri Oct 29 2010 Jan Pazdziora 1.2.18-1
- fix rpmlint error (msuchy@redhat.com)
- fix rpmlint error (msuchy@redhat.com)
- fix rpmlint error (msuchy@redhat.com)

* Mon Oct 25 2010 Jan Pazdziora 1.2.17-1
- To get UTF-8 strings in character semantics from DBD::Pg automatically, we
  have to enable it.
- Error in packages dependencies and obsoletes (PXT) (lzap+git@redhat.com)
- Sorting fix in packages for PostgreSQL (lzap+git@redhat.com)
- Reverting "Removed unnecessary ORDER BY" commits and fixing
  (lzap+git@redhat.com)

* Thu Oct 21 2010 Lukas Zapletal 1.2.16-1
- Sorting fix in packages for PostgreSQL
- Fix of evr_t_as_vre_simple PostgreSQL function
- Fix in package file list for PostgreSQL
- Changed SQL Perl generator joins to ANSI

* Wed Oct 20 2010 Lukas Zapletal 1.2.15-1
- Function evr_t_as_vre_simple in all package queries now general

* Wed Oct 20 2010 Lukas Zapletal 1.2.14-1
- Fix in PostgreSQL (of previous commit)
- All DECODE functions replaced with CASE-WHEN in System_queries
- Fixing system overview list for PostgreSQL
- Port /network/systems/details/custominfo/edit.pxt
- Port /network/systems/details/custominfo/index.pxt
- Update Perl module to redirect to Java not PXT
- s|/network/systems/ssm/misc/index.pxt|/rhn/systems/ssm/misc/Index.do|

* Wed Oct 13 2010 Jan Pazdziora 1.2.13-1
- 642203- Removed the Task Status page for it needs a serious work over with
  our new configs (paji@redhat.com)
- 631847 - in RHN Proxy 5.4 is used jabber 2.0 where user is called jabber
  (instead of jabberd) (msuchy@redhat.com)
- Port /network/systems/custominfo/delete.pxt (colin.coe@gmail.com)
- Port /network/systems/details/delete_confirm.pxt (colin.coe@gmail.com)

* Mon Oct 11 2010 Jan Pazdziora 1.2.12-1
- Fix indentation -- use spaces.
- Fix the ORA_BLOB issue which prevents spacewalk-schema from starting.
- 631847 - add keys for proxy 5.4 (msuchy@redhat.com)
- If host or port is not specified, we do not want to put those empty strings
  to the dbi:Pg: connect string.
- Since we use RHN::DataSource::Simple in Sniglets::ListView::ProbeList, we
  might just as well use it (I man, Perl use).

* Fri Oct 08 2010 Jan Pazdziora 1.2.11-1
- Move use DBD::Oracle to eval so that we do not get rpm dependencies
  populated.

* Wed Oct 06 2010 Jan Pazdziora 1.2.10-1
- Use current_timestamp instead of the Oracle-specific sysdate in
  set_cloned_from.
- To PostgreSQL, procedures are just functions, call them as such.
- We do not seem to be using the inout parameter anywhere in our code, remove
  the code to make porting to PostgreSQL easier.
- Use current_timestamp instead of the Oracle-specific sysdate in
  clone_channel_packages.
- Since we have trigger which sets rhnRepoRegenQueue.id since
  f2153167da508852183501f320c2e71c08a0441c, we can avoid .nextval.
- As PostgreSQL does not support table aliases in inserts, remove them.
- Make sequence_nextval method support PostgreSQL syntax.
- Do not reconnect with every sequence_nextval -- the $self should be usable
  object to call prepare on.
- Use the utility sequence_nextval method instead of direct
  rhn_channel_id_seq.nextval, to allow portable nextval operation.
- For PostgreSQL, we just select function(params) instead of begin...end block.
- 639449 - add package spacewalk-setup-jabberd to list of packages which should
  be removed in Proxy WebUI installer (msuchy@redhat.com)

* Tue Oct 05 2010 Jan Pazdziora 1.2.9-1
- Force the field names to be uppercase since that is what the application
  expects.
- Use case instead of decode, it is more portable.
- Mark aliases with AS. This is what PostgreSQL requires.
- Instead of checking user_objects which is not portable, just attempt to
  select from PXTSESSIONS directly.
- We first check if there is some object not named PLAN_TABLE, and then if
  there is some object named PXTSESSIONS. Just drop the first check.
- Port /network/account/activation_keys/child_channels.pxt
  (coec@war.coesta.com)
- Port /network/systems/ssm/system_list.pxt (coec@war.coesta.com)
- Port SSM Package Refresh Page (coec@war.coesta.com)
- Simple fixes (coec@war.coesta.com)
- Port /network/systems/ssm/index.pxt (colin.coe@gmail.com)
- Port HW refresh page (colin.coe@gmail.com)

* Mon Sep 27 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.8-1
- 636653 - Made the  Channel Family Subscribed Systems page show guest systems
  also (paji@redhat.com)
- make 'db-control report' report TEMP_TBS statistics (mzazrivec@redhat.com)
- 630585 - about-chat now points to proper channel (branding)
  (lzap+git@redhat.com)
- Cleanedup old/proted/unused config queries and updated the one for snapshot
  (paji@redhat.com)
- adding configchannel.lookupFileInfo() taking a revision id
  (jsherril@redhat.com)

* Fri Sep 10 2010 Partha Aji <paji@redhat.com> 1.2.7-1
- 629606 - Fixed a list tag check box issue (paji@redhat.com)
- 591899 - fixing error where cloning an already cloned channel would still
  result in errata showing up on the clone tab when managing it
  (jsherril@redhat.com)

* Fri Sep 10 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.6-1
- 630950 - fix ISE in proxy webUI installer

* Thu Sep 09 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.5-1
- 580080 - fix link to Proxy Guide

* Wed Sep 08 2010 Shannon Hughes <shughes@redhat.com> 1.2.4-1
- bug fixes for audit tab and proxy installer additions (shughes@redhat.com)

* Wed Sep 08 2010 Shannon Hughes <shughes@redhat.com> 1.2.3-1
- 589728 hide audit functionality for satellite product (shughes@redhat.com)

* Wed Sep 08 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.2-1
- 631847 - create 5.4 webUI installer
- 614918 - Made SSM Select Systems to work with I18n languages
  (paji@redhat.com)

* Wed Sep 01 2010 Jan Pazdziora 1.2.1-1
- 621479 - Fix missing duplicates menu (coec@war.coesta.com)
- Revert "Remove hardware.pxt" (colin.coe@gmail.com)
- Removal of unused code.
- System Notes pages PXT to java (colin.coe@gmail.com)
- bumping package versions for 1.2 (mzazrivec@redhat.com)

* Thu Aug 05 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.8-1
- Remove hardware.pxt
- Convert hardware.pxt to Java

* Wed Aug 04 2010 Jan Pazdziora 1.1.7-1
- Add system migration to webUI (colin.coe@gmail.com)

* Fri Jul 16 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.6-1
- 581812 - fixed file ordering

* Fri Jul 16 2010 Milan Zazrivec <mzazrivec@redhat.com> 1.1.5-1
- added a configuration page to orgs to handle maintenance windows
- cleaned up web_customer, rhnPaidOrgs and rhnDemoOrgs

* Thu Jul 01 2010 Miroslav Suchý <msuchy@redhat.com> 1.1.4-1
- channel nav support for repository mapping (shughes@redhat.com)
- Added flex magic to ChannelFamily -> Orgs page (paji@redhat.com)

* Mon Jun 21 2010 Jan Pazdziora 1.1.3-1
- Good Bye Channel License Code (paji@redhat.com)
- Removed unused code.
- Removed the bulk-subscribe and unsubscribe which is not used anywhere
  (paji@redhat.com)
- removed an unused method (paji@redhat.com)

* Mon May 31 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.2-1
- 577355 - fixing broken link on channel->errata->clone screen
- Setting server.nls_lang once, later in this file, should be enough.
- code cleanup - this configuration files are not used in proxy
- Removing web/conf/*.conf files that are not packages nor used.
- bump version for spacewalk 1.1
- Fixed a couple of links with respect to the delete confirm change..

* Mon Apr 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.1-1
- bumping spec files to 1.1 packages
- Constants DEFAULT_RHN_SATCON_TREE and DEFAULT_SATCON_DICT not longer used

* Wed Mar 31 2010 Miroslav Suchý <msuchy@redhat.com> 0.9.7-1
- 576907 - make SystemSnapshots aware of multiarch packages

* Thu Mar 25 2010 Justin Sherrill <jsherril@redhat.com> 0.9.6-1
- 528170 - fixing issue where cloning a channel with cloned errata would select
  clones of the cloned errata to pull into the new channel if they existed,
  instead of just using the original clones directly. (jsherril@redhat.com)

* Thu Mar 18 2010 Jan Pazdziora 0.9.5-1
- 568958 - fixing issue where package removal and verify could not be scheduled
  or would not work for systems that do not upload arch information
  (jsherril@redhat.com)
- 516048 - syncing java stack with perl stack on channel naming convention
  (shughes@redhat.com)
- 529371 - use the OO interface to File::Temp, make it UNLINK

* Wed Mar 10 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.4-1
- fixed typos

* Mon Mar 08 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.3-1
- 529371 - fixed missing code from gpg migration
- 528170 - fixing cloning on an already cloned channel

* Fri Feb 19 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.1-1
- moved PXT::Debug to separate module

* Thu Feb 04 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.14-1
- updated copyrights
- removed a lot of unused code

* Tue Feb 02 2010 Jan Pazdziora 0.8.13-1
- 549666 - link to the list of keys handled by the Java stack.
- Removal of dead code.

* Mon Feb 01 2010 Jan Pazdziora 0.8.11-1
- Removed RSS unused code.
- 492161 - removed web/html/errata.
- Removed a lot of code made unused by above removals.

* Fri Jan 29 2010 Miroslav Suchý <msuchy@redhat.com> 0.8.10-1
- No XMLRPC/SOAP processing in the web/Perl stack,
  removing. (jpazdziora@redhat.com)
- 543879 - adding support to the proxy side to redirect to a url
  that will rewrite kickstarts with the proxy name for /cblr
  urls (jsherril@redhat.com)


* Thu Jan 14 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.9-1
- force correct UTF-8 in changelog
- fixed directories and links listing in package detail
- fixed email sending in pxt pages
- added back RHN::Cleansers
- removed dead code

* Wed Jan 06 2010 Jan Pazdziora 0.8.8-1
- Fixed the forgot_* emails.
- More dead code removals.

* Mon Jan 04 2010 Michael Mraka <michael.mraka@redhat.com> 0.8.6-1
- more dead code removed
* Sat Dec 26 2009 Jan Pazdziora 0.8.5-1
- more dead code removals

* Tue Dec 22 2009 Jan Pazdziora 0.8.4-1
- Removed more dead code, including spacewalk-cypress.

* Mon Dec 21 2009 Jan Pazdziora <jpazdziora@redhat.com> 0.8.3-1
- removed a lot of dead code, including spacewalk-moon
- modified to fit sha256 schema changes (michael.mraka@redhat.com)
- adding channel.software.regenerateYumCache() api call (jsherril@redhat.com)

* Tue Dec 15 2009 Jan Pazdziora 0.8.2-1
- Removed dead code (PXT tags, xmlrpc, functions, modules).

* Fri Dec  4 2009 Miroslav Suchý <msuchy@redhat.com> 0.8.1-1
- sha256 support

* Wed Dec 02 2009 Tomas Lestach <tlestach@redhat.com> 0.7.8-1
- 537094 - yum list-sec CVE's on cloned channels doesn't work
  (tlestach@redhat.com)

* Mon Nov 30 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.7-1
- add variable web.chat_enabled to config file

* Thu Nov 19 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.6-1
- 531649 - fixed confirmation message after channel merge/compare
- 527881 - fixed set clearing on the channel merge page

* Mon Oct 26 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.5-1
- bump up spacewalk version to 0.7
- 449167 - add api call for rpm install date
- Make spacewalk use the editarea RPM and remove supplied editarea files <colin.coe@gmail.com>

* Thu Sep 17 2009 Miroslav Suchý <msuchy@redhat.com> 0.7.4-1
- 476851 - removal of tables: rhn_db_environment, rhn_environment
- 520441 - don't apply ExtUtils::MY->fixin(shift) to perl executables

* Tue Sep 01 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.3-1
- 488431 - don't report high usage on UNDO

* Fri Aug 28 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.2-1
- awk | sed | sed is rarely needed
- use spacewalk-cfg-get instead of awk

* Thu Aug 20 2009 Miroslav Suchy <msuchy@redhat.com> 0.7.1-1
- fix an ISE relating to config management w/selinux (Joshua Roys)
- allow users to chat with spacewalk members on IRC via the web. (jesusr@redhat.com)
- 516608 - redirect output of rhn-ssl-tool to apache error log

* Wed Aug 05 2009 John Matthews <jmatthew@redhat.com> 0.6.19-1
- 515580 - remove hard links to scooby.rdu (shughes@redhat.com)

* Tue Aug 04 2009 Jan Pazdziora 0.6.17-1
- Bump up the version to 0.6, in preparation for Spacewalk 0.6

* Wed Jul 29 2009 John Matthews <jmatthew@redhat.com> 0.6.16-1
- 512440 - SetHandler to none to allow ProxyPass on /cobbler* and /cblr to
  work. (jpazdziora@redhat.com)
- 512440 - Revert parts of "512440 - Fixed the proxies to turn SSLProxyEngine
  to deal with Cobbler KS files" (jpazdziora@redhat.com)
- 512440 - Revert "512440 - Fixed the proxies to turn SSLProxyEngine to deal
  with Cobbler KS files" (jpazdziora@redhat.com)
-  Adding a new create channel api using checksumtype as a params.
  (pkilambi@redhat.com)

* Mon Jul 27 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.15-1
- Prep perl stack for PostgreSQL connections. (dgoodwin@redhat.com)
- Remove use of RHN_DEFAULT_DB environment variable for db connections.
  (dgoodwin@redhat.com)
- Remove unused get_default_handle sub in DB.pm. (dgoodwin@redhat.com)

* Mon Jul 27 2009 John Matthews <jmatthew@redhat.com> 0.6.14-1
- 512440 - Fixed the proxies to turn SSLProxyEngine to deal with Cobbler KS
  files (paji@redhat.com)
- 512440 - Fixed the proxies to turn SSLProxyEngine to deal with Cobbler KS
  files (paji@redhat.com)
- 493060 - do not send email "RHN Monitoring Scout started" by default
  (msuchy@redhat.com)

* Tue Jul 21 2009 Miroslav Suchy <msuchy@redhat.com> 0.6.13-1
- 512440 - add cobbler-proxy.conf to older rhn proxy installer

* Thu Jul 09 2009 John Matthews <jmatthew@redhat.com> 0.6.11-1
- 510146 - Update copyright years from 2002-08 to 2002-09.
  (dgoodwin@redhat.com)
- 508980 - converting SSM kickstart to java (jsherril@redhat.com)

* Mon Jul 06 2009 John Matthews <jmatthew@redhat.com> 0.6.10-1
- 509376 - add Shared Channels to side navigation of Channels tab
  (bbuckingham@redhat.com)
- 508859 - fixed proxy documenation links (shughes@redhat.com)

* Thu Jun 25 2009 John Matthews <jmatthew@redhat.com> 0.6.9-1
- 506154 - Added "wrap" option to textarea widget. Set to off for remote
  command script editing page. (jason.dobies@redhat.com)
- 501933 - Changed the script rendering to wrap in a readonly textarea.
  (jason.dobies@redhat.com)
- 505315 - checking in missing file from previous commit (jsherril@redhat.com)
- 505315 - fixing issue where cobbler provisioning couldnt occur through a 5.3
  proxy if installed through the webui (jsherril@redhat.com)
- 502259 - fixing issue where systems would not show up on applicable systems
  page of patches (jsherril@redhat.com)
- 504327 - fixing acl for chcecking needed install tab (shughes@redhat.com)
- 503187 - set MaxRequestsPerChild to 200 (WebUI installer) (msuchy@redhat.com)

* Fri Jun 05 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.8-1
- 197294 - add hardware report support for CAPTURE cards (shughes@redhat.com)
- 500709 - html error code page support for sessionless bots (shughes@redhat.com)
- 435043 - adding errata sync page for syncing out of date errata (that have
  been updated by red hat) (jsherril@redhat.com)
- 501784 - fixed issue with timed out logins that required cookie deletion to
  log in again (jsherril@redhat.com)
- 501224 - api - enhance system.listSystemEvents to include more detail on
  events executed (bbuckingham@redhat.com)
- 500709 - static html for non session error pages (shughes@redhat.com)
- 503081 - fixed /help url to to go to /rhn/help/index.do instead of about.pxt
  (paji@redhat.com)
- 503081 - Fixed a html redirect issue causing page to reload indefinitely on
  IE (paji@redhat.com)
- 501784 - fixed issue with timed out logins that required cookie deletion to
  log in again (jsherril@redhat.com)
- 501797 - remove /etc/rc.d/np.d/step MonitoringScout install
  (msuchy@redhat.com)
- 499399 - create new api call proxy.createMonitoringScout (msuchy@redhat.com)
- 496105 - Fix for setting up activaiton key for para-host provisioning
  (paji@redhat.com)
- 498467 - A few changes related to the channel name limit increase.
  (jason.dobies@redhat.com)

* Tue May 26 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.7-1
- 500429 - removed join against rhnSharedChannelView to remove dup entries
  (shughes@redhat.com)
- Clear selected packages when merging channel contents. (dgoodwin@redhat.com)
- 494966 - don't allow users to clone shared channels (shughes@redhat.com)

* Thu May 21 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.6-1
- 501376 - api - deprecate system.applyErrata (bbuckingham@redhat.com)
- 499667 - Implemented option 2 presented in the BZ: allow comparision of any
  channel to *any* channel, ignore arch all together. (jason.dobies@redhat.com)
- Fixed sorting to use javascript (paji@redhat.com)
- 500719 - Ported delete channel page to Java; success/failure messages now
  properly displayed on manage channels page. (jason.dobies@redhat.com)
- 498251 - add new api proxy.listAvailableProxyChannels (msuchy@redhat.com)
- 500499 - fixed issue where task engine times were not displayed, the old perl
  code had been ripped out, so i converted it to java (jsherril@redhat.com)
- 498282 - rhns-proxy-monitoring has been renamed to spacewalk-proxy-monitoring
  (msuchy@redhat.com)
- 497892 - create access.log on rhel5 (msuchy@redhat.com)
- 499473 - api - added 2 new api calls to org for listing entitlements
  (bbuckingham@redhat.com)
- 492588 - added left outer join to include shared channels
  (shughes@redhat.com)
- 499377 - fix help link for proxy install (bbuckingham@redhat.com)

* Wed May  6 2009 Miroslav Suchý <msuchy@redhat.com> 0.6.5-1
- make webui proxy installer aware of new packages spacewalk-monitoring-selinux
- make webui proxy installer aware of new packages oracle-instantclient-selinux, oracle-nofcontext-selinux
- 493428 - make webui installer aware of new package - spacewalk-proxy-selinux
- 492588 - changed query to use rhnSharedChannelView to support shared channels in activation keys
- 480011 - Added organization to the top header near the username.
- 481578 - Ported manage software channels page from perl to java
- 489902 - fix help links to work with rhn-il8n-guides

* Fri Apr 24 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.4-1
- 485981 - fix web proxy installer help links (bbuckingham@redhat.com)

* Wed Apr 22 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.3-1
- 485020 - errata clone names consistent in perl/java (jsherril@redhat.com)
- 474567 - Stop running commands on SSM systems that don't have provisioning. (dgoodwin@redhat.com)
- 436851 - Removed dead references (jason.dobies@redhat.com)
- 496710 - system.listSystemEvents - convert dates in return to use Date (bbuckingham@redhat.com)
- 496214 - Fix About links in Perl sitenav. (dgoodwin@redhat.com)

* Fri Apr 17 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.2-1
- 496161 - removing find a system box from system group details page
  (jsherril@redhat.com)
- 476248 - add correct lang to proxy install guide url (jesusr@redhat.com)
- 494450 - api - add permissions_mode to ConfigRevisionSerializer & fix doc on
  system.config.createOrUpdatePath (bbuckingham@redhat.com)

* Thu Apr 16 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.1-1
- remove Proxy Release Notes link and unused Developer's area. (jesusr@redhat.com)
- 494714 - fixing 404 after cloning channel with selective errata (jsherril@redhat.com)
- 484294 - can't delete channel with distros (paji@redhat.com)
- 495722 - fixing issue where /ty/TOKEn wasnt being rendered properly (jsherril@redhat.com)
- 490904 - change all references to /rhn/help/*/en/ -> /rhn/help/*/en-US/ (jesusr@redhat.com)
- api doclet - enhanced to support a 'since' tag, tagged snapshot apis and
  bumped api version (bbuckingham@redhat.com)
- 494475,460136 - remove faq & feedback code which used customerservice emails. (jesusr@redhat.com)
- Revert "484702 - remove dead function generate_server_pem from RHN::SatInstall." (mzazrivec@redhat.com)
- Revert "484703 - remove dead function generate_satcon_dict from RHN::SatInstall." (mzazrivec@redhat.com)
- Revert "484705 - remove dead function satcon_deploy from RHN::SatInstall." (mzazrivec@redhat.com)
- bump Versions to 0.6.0 (jesusr@redhat.com)

* Thu Mar 26 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.23-1
- 489736 - generate non-expiring kickstart package download url
- 489736 - download_url_lifetime of 0 disables expiration server wide
- 489736 - can disable experiation by package name by non_expirable_package_urls

* Thu Mar 26 2009 Miroslav Suchy <msuchy@redhat.com> 0.5.22-1
- 491667 - do not fail if none of the packages are installed
- code cleanup - remove 3.6 and 3.7 proxy installer (EOL)
- 491670 - add rhn-proxy-branding to list of package to remove in 5.3
- 491670 - add conflicting package from older proxy versions
- remove libidn from conflictin packages from proxy installer

* Wed Mar 25 2009 Jan Pazdziora 0.5.20-1
- 491687 - call wrapper around sudo invocations, to change SELinux domain

* Fri Mar 20 2009 Mike McCune <mmccune@gmail.com> 0.5.19-1
- space05 - bumping release footer/config for 0.5 release

* Thu Mar 19 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.18-1
- 472595 - fixes for kickstart performance, start of porting ks downloads to java
- 490726 - minor updates to about.pxt
- added support for db-control extend TEMP_TBS
- 466502 - fixes issues related to repo command addition and proper ks url generation

* Thu Mar 12 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.17-1
- forgot to remove an alert, arg

* Wed Mar 11 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.16-1
- 249459 - fixing issue where org trust page was busted
- 481236 - fix issue where rewrite was not being inherited by virtual host, making package downloads didn't work
- 483287 - Added ability to do a cobbler sync thru the UI
- 465775 - adding synopsis to errata clone page
- Use /usr/sbin/rhn-satellite for restart
- Revert "code cleanup - enable_notification_cron and disable_notification_ cron are not used any more"

* Thu Mar 05 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.15-1
- 487563 - switching take_snapshots to enable_snapshots
- 193788 - converting a few pages to java, so we can sort better
- 459827 - mention the 64 character limit.
- 485497 - adding IQ back to t6 list
- 487563 - adding on/off switch for snapshots

* Thu Feb 26 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.14-1
- rebuild

* Thu Feb 19 2009 Miroslav Suchy <msuchy@redhat.com> 0.5.13-1
- fix proxy webui installer

* Thu Feb 19 2009 Jan Pazdziora 0.5.12-1
- 479742 - changes to make doc links from Help and About pages configurable (Brad B.)
- 486057 - reworked proxy install xml file for 530 support (Shannon H.)
- 485878 - missing options in db-control.1 (Milan Z.)
- 485985 - remove references to obsolete package rhns-proxy-management (Shannon H.)
- 484717 - remove dead function store_ssl_cert from RHN::SatInstall
- 484709 - remove dead function sat_sync from RHN::SatInstall
- 484705 - remove dead function satcon_deploy from RHN::SatInstall
- 484703 - remove dead function generate_satcon_dict from RHN::SatInstall
- 484702 - remove dead function generate_server_pem from RHN::SatInstall
- 484701 - remove dead function deploy_ca_cert from RHN::SatInstall
- 484685 - remove dead function install_server_cert from RHN::SatInstall
- 484681 - remove dead function populate_tablespace_name from RHN::SatInstall
- 484699 - remove dead function populate_database from RHN::SatInstall
- 484680 - remove dead function write_tnsnames from RHN::SatInstall
- code cleanup: remove acl="global_config(satellite)" (Miroslav S.)
- code cleanup - remove unreachable pages (old hosted content) (Miroslav S.)

* Mon Feb 16 2009 Pradeep Kilambi <pkilambi@redhat.com> 0.5.11-1
- yum repodata regen changes to taskomatic

* Thu Feb 12 2009 Jan Pazdziora 0.5.10-1
- code cleanup - enable_notification_cron, disable_notification_cron,
  monitoring_available are not used any more (Miroslav S.)
- 483798 - added index.pxt to catch redirect to perl files, and
  direct to the docs base page (about.pxt) (Jason D.)
- 482926 - fixed webui proxy activation (Shannon H.)
- 484481 - 2nd part of errata cloning patch, with modification to pull
  in all but the first two characters (Justin S.)
- 484481 - patch to make errata clone names more consistent ((Justin S.)
- 426472 - replacing grep | awk with awk
- 483606 - incorporated UI feedback and moved link to status to leftnav,
  making each status filter its own context tab (Jason D.)

* Thu Feb 05 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.9-1
- 483603 - First pass at display of async SSM operations in the UI

* Wed Feb 04 2009 Devan Goodwin <dgoodwin@redhat.com> 0.5.8-1
- Remove favicon.ico. (moved to branding rpm)

* Fri Jan 30 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.7-1
- 483058 - subscribe to proxy channel if requested

* Thu Jan 29 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.6-1
- 482926 - fix proxy webui installer

* Wed Jan 28 2009 Dennis Gilmore <dennis@ausil.us> 0.5.4-1
- use %%files correctly
- make sure perl modules get installed in %%{perl_vendorlib}
- add provides for Obsoletes

* Thu Jan 22 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.3-1
- 468180 - warn that after proxy deactivation user should run rhn_check

* Wed Jan 21 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.2-1
- 480894 - add to Channel.pm 5.3 channels

* Tue Jan 20 2009 Miroslav Suchý <msuchy@redhat.com> 0.5.1-1
- add proxy 5.3 webui installer
- 480328 - rhn-proxy is not service any more

* Thu Jan 15 2009 Jan Pazdziora 0.4.18-1
- 479948 - add missing use RHN::Mail

* Mon Jan 12 2009 Mike McCune <mmccune@gmail.com> 0.4.17-1
- adding editarea as reqquired by Colin.Coe@woodside.com.au's patches coming up.
- 479738 - update Help to point to the help page
- 479600 - fixed typo

* Mon Jan 12 2009 Michael Mraka <michael.mraka@redhat.com> 0.4.16-1
- resolved #479600

* Thu Jan 08 2009 Mike McCune <mmccune@gmail.com> 0.4.15-1
- spacewalk-httpd removal and latest changes

* Wed Jan  7 2009 Michael Mraka <michael.mraka@redhat.com> 0.4.14-1
- fixed db-control shrink-segments

* Mon Dec 22 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.13-1
- added product_name branding

* Thu Dec 18 2008 Jan Pazdziora 0.4.12-1
- 461162 - adding support for cobbler auth for taskomatic that actually works
- more fixes for the $sth variable

* Thu Dec 18 2008 Jan Pazdziora 0.4.10-1
- WebUI will report Spacewalk release 0.4
- fixing duplicated $sth variable

* Wed Dec 17 2008 Jesus M. Rodriguez <jesusr@redhat.com> 0.4.9-1
- 476893 - update perl package verify access query to be multiorg aware
- 461593 - fixing web site nav for package details

* Wed Dec 17 2008 Miroslav Suchý <msuchy@redhat.com> 0.4.8-1
- 226915 - db_name can be different from db instance name

* Wed Dec 17 2008 Miroslav Suchy <msuchy@redhat.com> 0.4.7-1
- 476812 - monitoring should be aware of multiorg

* Mon Dec  8 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.6-1
- resolved #474545 - fixed Obsoletes

* Fri Nov 28 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.5-1
- removed rhn-database
- resolved #472563 - fidex error in db-control extend

* Thu Nov 20 2008 Miroslav Suchy <msuchy@redhat.com> 0.4.2-1
- 472346 - Bump up API version and make the versioning independent on web.version

* Wed Oct 29 2008 Michael Mraka <michael.mraka@redhat.com> 0.3.4-1
- resolved #468153 - fixed in, out fd handling

* Thu Oct 23 2008 Michael Mraka <michael.mraka@redhat.com> 0.3.3-1
- fixed #467877 - use runuser instead of su
- fixed #467512 - db-control man page

* Wed Sep 24 2008 Milan Zazrivec 0.3.1-1
- bumped versions for spacewalk 0.3
- fixed package obsoletes

* Wed Sep  3 2008 Mike McCune 0.2.3-1
- bumping rhn_web.conf version to 0.2

* Fri Aug 29 2008 Jesus M. Rodriguez <jesusr@redhat.com 0.2.2-1
- fix release
- remove remnants of test-conn

* Wed Aug 13 2008 Mike McCune <mmccune@redhat.com 0.2-1
- fix Requires: statement to reflect new spacewalk-pxt name

* Mon Aug  4 2008 Miroslav Suchy <msuchy@redhat.com> 0.2-0
- rename package from rhn-* to spacewalk-*
- clean up spec

* Fri Jun  6 2008 Miroslav Suchy <msuchy@redhat.com> - 5.2.0-10
- add support for proxy on RHEL5

* Wed May 21 2008 Jan Pazdziora 5.2.0-7
- changing perl-Time-HiRes to perl(Time::HiRes)
- changing mod_jk-ap20 to mod_proxy_ajp.so on RHEL 5

* Tue May 20 2008 Michael Mraka <michael.mraka@redhat.com> 5.2.0-5
- added stats options to db-control

* Fri May 16 2008 Jan Pazdziora - 5.2.0-4
- rebuilt with latest code

* Wed Apr 30 2008 Jan Pazdziora <jpazdziora@redhat.com> 5.2.0-3
- rebuilt via brew / dist-cvs

* Thu Sep  6 2007 Jan Pazdziora <jpazdziora@redhat.com>
- updated to use default httpd from distribution and mod_perl 2

* Mon May 1 2006 Partha Aji <paji@redhat.com>
- Added a cron job that checks the oracle table/space usage and emails it to the user. (Bug 182054)

* Mon Nov  7 2005 Robin Norwood <rnorwood@redhat.com>
- Remove rhn-swab, because it annoys taw

* Thu Aug  8 2002 Cristian Gafton <gafton@redhat.com>
- unified all web stuff into a single src.rpm

* Thu Mar 14 2002 Chip Turner <cturner@minbar.devel.redhat.com>
- updated for the new bs

* Thu Jun 21 2001 Cristian Gafton <gafton@redhat.com>
- build system changes

* Mon Jun  4 2001 Cristian Gafton <gafton@redhat.com>
- created first package
