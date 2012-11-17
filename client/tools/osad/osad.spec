%global rhnroot /usr/share/rhn
%global rhnconf /etc/sysconfig/rhn
%global client_caps_dir /etc/sysconfig/rhn/clientCaps.d

%if 0%{?suse_version}
%global apache_group www
%global include_selinux_package 0
%else
%global apache_group apache
%global include_selinux_package 1
%endif

%if 0%{?suse_version}
%define apache_group www
%else
%define apache_group apache
%endif

Name: osad
Summary: Open Source Architecture Daemon
Group:   System Environment/Daemons
License: GPLv2
URL:     https://fedorahosted.org/spacewalk
Source0: https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
Version: 5.10.41.6
Release: 1%{?dist}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python-devel
Requires: python
Requires: rhnlib >= 2.5.38
Requires: jabberpy
Requires: rhn-client-tools >= 1.3.7
%if 0%{?suse_version} && 0%{?suse_version} < 1110 || 0%{?rhel} && 0%{?rhel} <= 5
Requires: python-hashlib
%endif
%if 0%{?suse_version} >= 1140
Requires: python-xml
%else
# This should have been required by rhnlib
Requires: PyXML
%endif
Conflicts: osa-dispatcher < %{version}-%{release}
Conflicts: osa-dispatcher > %{version}-%{release}
%if !0%{?suse_version}
Requires(post): chkconfig
Requires(preun): chkconfig
Requires: jabberpy
# This is for /sbin/service
Requires(preun): initscripts
%else
# provides chkconfig on SUSE
Requires(post): aaa_base
Requires(preun): aaa_base
# to make chkconfig test work during build
BuildRequires: sysconfig syslog
Requires: python-jabberpy
Requires(preun): %fillup_prereq %insserv_prereq
%endif

%description
OSAD agent receives commands over jabber protocol from Spacewalk Server and
commands are instantly executed.

This package effectively replaces the behavior of rhnsd/rhn_check that
only poll the Spacewalk Server from time to time.

%package -n osa-dispatcher
Summary: OSA dispatcher
Group:    System Environment/Daemons
Requires: spacewalk-backend-server >= 1.2.32
Requires: jabberpy
Requires: lsof
Conflicts: %{name} < %{version}-%{release}
Conflicts: %{name} > %{version}-%{release}
%if !0%{?suse_version}
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
%else
# provides chkconfig on SUSE
Requires(post): aaa_base
Requires(preun): aaa_base
Requires(preun): %fillup_prereq %insserv_prereq
%endif

%description -n osa-dispatcher
OSA dispatcher is supposed to run on the Spacewalk server. It gets information
from the Spacewalk server that some command needs to be execute on the client;
that message is transported via jabber protocol to OSAD agent on the clients.

%if 0%{?include_selinux_package}
%package -n osa-dispatcher-selinux
%global selinux_variants mls strict targeted
%global selinux_policyver %(sed -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp 2> /dev/null)
%global POLICYCOREUTILSVER 1.33.12-1

%global moduletype apps
%global modulename osa-dispatcher

Summary: SELinux policy module supporting osa-dispatcher
Group: System Environment/Base
BuildRequires: checkpolicy, selinux-policy-devel, hardlink
BuildRequires: policycoreutils >= %{POLICYCOREUTILSVER}
Requires: spacewalk-selinux

%if "%{selinux_policyver}" != ""
Requires: selinux-policy >= %{selinux_policyver}
%endif
%if 0%{?rhel} == 5
Requires:        selinux-policy >= 2.4.6-114
%endif
Requires(post): /usr/sbin/semodule, /sbin/restorecon, /usr/sbin/selinuxenabled, /usr/sbin/semanage
Requires(postun): /usr/sbin/semodule, /sbin/restorecon, /usr/sbin/semanage, spacewalk-selinux
Requires: osa-dispatcher

%description -n osa-dispatcher-selinux
SELinux policy module supporting osa-dispatcher.
%endif

%prep
%setup -q
%if 0%{?suse_version}
cp prog.init.SUSE prog.init
%endif

%build
make -f Makefile.osad all

%if 0%{?include_selinux_package}
%{__perl} -i -pe 'BEGIN { $VER = join ".", grep /^\d+$/, split /\./, "%{version}.%{release}"; } s!\@\@VERSION\@\@!$VER!g;' osa-dispatcher-selinux/%{modulename}.te
for selinuxvariant in %{selinux_variants}
do
    make -C osa-dispatcher-selinux NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
    mv osa-dispatcher-selinux/%{modulename}.pp osa-dispatcher-selinux/%{modulename}.pp.${selinuxvariant}
    make -C osa-dispatcher-selinux NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{rhnroot}
make -f Makefile.osad install PREFIX=$RPM_BUILD_ROOT ROOT=%{rhnroot} INITDIR=%{_initrddir}
mkdir -p %{buildroot}%{_var}/log/rhn
touch %{buildroot}%{_var}/log/osad
touch %{buildroot}%{_var}/log/rhn/osa-dispatcher.log

%if 0%{?include_selinux_package}
for selinuxvariant in %{selinux_variants}
  do
    install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
    install -p -m 644 osa-dispatcher-selinux/%{modulename}.pp.${selinuxvariant} \
           %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{modulename}.pp
  done

# Install SELinux interfaces
install -d %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 osa-dispatcher-selinux/%{modulename}.if \
  %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}/%{modulename}.if

# Hardlink identical policy module packages together
/usr/sbin/hardlink -cv %{buildroot}%{_datadir}/selinux

# Install osa-dispatcher-selinux-enable which will be called in %%post
install -d %{buildroot}%{_sbindir}
install -p -m 755 osa-dispatcher-selinux/osa-dispatcher-selinux-enable %{buildroot}%{_sbindir}/osa-dispatcher-selinux-enable
%endif

mkdir -p %{buildroot}%{_var}/log/rhn
touch %{buildroot}%{_var}/log/osad
touch %{buildroot}%{_var}/log/rhn/osa-dispatcher.log

# add rclinks
ln -sf ../../etc/init.d/osad %{buildroot}%{_sbindir}/rcosad
ln -sf ../../etc/init.d/osa-dispatcher %{buildroot}%{_sbindir}/rcosa-dispatcher

%if 0%{?suse_version}
%py_compile %{buildroot}/%{rhnroot}
%py_compile -O %{buildroot}/%{rhnroot}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if 0%{?suse_version}

%preun
%stop_on_removal osad

%post
ARG=$1
%{fillup_and_insserv -f -y osad}
if [ $ARG -eq 1 ] ; then
  # executed only in case of install
  /etc/init.d/osad start ||:
fi

%postun
%restart_on_update osad
%{insserv_cleanup}

%preun -n osa-dispatcher
%stop_on_removal osa-dispatcher

%post -n osa-dispatcher
%{fillup_and_insserv osa-dispatcher}

%postun -n osa-dispatcher
%restart_on_update osa-dispatcher
%{insserv_cleanup}

%else

%post
if [ -f %{_sysconfdir}/init.d/osad ]; then
    /sbin/chkconfig --add osad
fi

%preun
if [ $1 = 0 ]; then
    /sbin/service osad stop > /dev/null 2>&1
    /sbin/chkconfig --del osad
fi

%post -n osa-dispatcher
if [ -f %{_sysconfdir}/init.d/osa-dispatcher ]; then
    /sbin/chkconfig --add osa-dispatcher
fi

%if %{include_selinux_package}
%preun -n osa-dispatcher
if [ $1 = 0 ]; then
    /sbin/service osa-dispatcher stop > /dev/null 2>&1
    /sbin/chkconfig --del osa-dispatcher
fi

%if 0%{?include_selinux_package}
%post -n osa-dispatcher-selinux
if /usr/sbin/selinuxenabled ; then
   %{_sbindir}/osa-dispatcher-selinux-enable
fi

%posttrans -n osa-dispatcher-selinux
#this may be safely remove when BZ 505066 is fixed
if /usr/sbin/selinuxenabled ; then
  rpm -ql osa-dispatcher | xargs -n 1 /sbin/restorecon -rvi {}
  /sbin/restorecon -vvi /var/log/rhn/osa-dispatcher.log
fi

%postun -n osa-dispatcher-selinux
# Clean up after package removal
if [ $1 -eq 0 ]; then

  /usr/sbin/semanage port -ln \
    | perl '-F/,?\s+/' -ane 'print map "$_\n", @F if shift @F eq "osa_dispatcher_upstream_notif_server_port_t" and shift @F eq "tcp"' \
    | while read port ; do \
      /usr/sbin/semanage port -d -t osa_dispatcher_upstream_notif_server_port_t -p tcp $port || :
    done
  for selinuxvariant in %{selinux_variants}
    do
      /usr/sbin/semodule -s ${selinuxvariant} -l > /dev/null 2>&1 \
        && /usr/sbin/semodule -s ${selinuxvariant} -r %{modulename} || :
    done
fi

rpm -ql osa-dispatcher | xargs -n 1 /sbin/restorecon -rvi {}
/sbin/restorecon -vvi /var/log/rhn/osa-dispatcher.log
%endif

%endif
%endif

%files
%defattr(-,root,root)
%dir %{rhnroot}/osad
%attr(755,root,root) %{_sbindir}/osad
%{rhnroot}/osad/__init__.py*
%{rhnroot}/osad/_ConfigParser.py*
%{rhnroot}/osad/jabber_lib.py*
%{rhnroot}/osad/osad.py*
%{rhnroot}/osad/osad_client.py*
%{rhnroot}/osad/osad_config.py*
%{rhnroot}/osad/rhn_log.py*
%config(noreplace) %{_sysconfdir}/sysconfig/rhn/osad.conf
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/rhn/osad-auth.conf
%config(noreplace) %{client_caps_dir}/*
%attr(755,root,root) %{_initrddir}/osad
%doc LICENSE
%{_sbindir}/rcosad
%config(noreplace) %{_sysconfdir}/logrotate.d/osad
%ghost %attr(600,root,root) %{_var}/log/osad
%if 0%{?suse_version}
# provide directories not owned by any package during build
%dir %{rhnroot}
%dir %{_sysconfdir}/sysconfig/rhn
%dir %{_sysconfdir}/sysconfig/rhn/clientCaps.d
%endif

%files -n osa-dispatcher
%defattr(-,root,root)
%dir %{rhnroot}/osad
%attr(755,root,root) %{_sbindir}/osa-dispatcher
%{rhnroot}/osad/__init__.py*
%{rhnroot}/osad/jabber_lib.py*
%{rhnroot}/osad/osa_dispatcher.py*
%{rhnroot}/osad/dispatcher_client.py*
%{rhnroot}/osad/rhn_log.py*
%config(noreplace) %{_sysconfdir}/sysconfig/osa-dispatcher
%config(noreplace) %{_sysconfdir}/logrotate.d/osa-dispatcher
%{rhnroot}/config-defaults/rhn_osa-dispatcher.conf
%dir %{_sysconfdir}/rhn/tns_admin
%dir %{_sysconfdir}/rhn/tns_admin/osa-dispatcher
%config(noreplace) %{_sysconfdir}/rhn/tns_admin/osa-dispatcher/sqlnet.ora
%attr(755,root,root) %{_initrddir}/osa-dispatcher
%attr(770,root,%{apache_group}) %dir %{_var}/log/rhn/oracle
%attr(770,root,root) %dir %{_var}/log/rhn/oracle/osa-dispatcher
%doc LICENSE
%{_sbindir}/rcosa-dispatcher
%ghost %attr(640,apache,root) %{_var}/log/rhn/osa-dispatcher.log
%if 0%{?suse_version}
%dir %attr(750, root, %{apache_group}) %{_sysconfdir}/rhn
%attr(755,root,%{apache_group}) %dir %{rhnroot}/config-defaults
%dir %{_sysconfdir}/rhn/tns_admin
%attr(770,root,%{apache_group}) %dir %{_var}/log/rhn
%endif

%if 0%{?include_selinux_package}
%files -n osa-dispatcher-selinux
%defattr(-,root,root,0755)
%doc osa-dispatcher-selinux/%{modulename}.fc
%doc osa-dispatcher-selinux/%{modulename}.if
%doc osa-dispatcher-selinux/%{modulename}.te
%{_datadir}/selinux/*/%{modulename}.pp
%{_datadir}/selinux/devel/include/%{moduletype}/%{modulename}.if
%doc LICENSE
%attr(0755,root,root) %{_sbindir}/osa-dispatcher-selinux-enable
%endif

%changelog
* Fri Mar 02 2012 Jan Pazdziora 5.10.41-1
- Update the copyright year info.

* Thu Mar 01 2012 Miroslav Suchý 5.10.40-1
- creating files for %%ghost should be done in %%install instead of %%build

* Wed Feb 29 2012 Miroslav Suchý 5.10.39-1
- log file may contain password, set chmod to 600
- by default log to /var/log/osad
- /etc/rhn/tns_admin/osa-dispatcher is directory, not config file
- fix typo in description
- mark log file osa-dispatcher.log as ghost owned
- add logrotate for /var/log/osad and own this file (as ghost)

* Thu Feb 23 2012 Michael Mraka <michael.mraka@redhat.com> 5.10.38-1
- we are now just GPL

* Tue Feb 07 2012 Jan Pazdziora 5.10.35-1
- Make sure that in case only NETWORKING_IPV6 is set, we do not get bash 'unary
  operator expected' error (jhutar@redhat.com)

* Wed Dec 21 2011 Milan Zazrivec <mzazrivec@redhat.com> 5.10.34-1
- update copyright info

* Wed Dec 21 2011 Michael Mraka <michael.mraka@redhat.com> 5.10.33-1
- python 2.4 on RHEL5 don't know 'with' block

* Tue Dec 20 2011 Milan Zazrivec <mzazrivec@redhat.com> 5.10.32-1
- Update db with new dispatcher password

* Tue Dec 20 2011 Michael Mraka <michael.mraka@redhat.com> 5.10.31-1
- don't print double [OK] when restarting
- turn off DeprecationWarning for jabber module

* Fri Dec 16 2011 Michael Mraka <michael.mraka@redhat.com> 5.10.30-1
- 756761 - reconnect if jabber server returns error during handshake

* Fri Dec 09 2011 Jan Pazdziora 5.10.29-1
- 691847, 664491 - adding tcp_keepalive_timeout and tcp_keepalive_count options
  to osad.conf.
- 691847, 664491 - read the keepalive settings from osad.conf and apply them to
  the osad socket.

* Fri Dec 02 2011 Jan Pazdziora 5.10.28-1
- Using password_in for parameter name to avoid confusion.

* Mon Nov 28 2011 Miroslav Suchý 5.10.27-1
- specify missing param password (mc@suse.de)

* Fri Nov 25 2011 Jan Pazdziora 5.10.26-1
- The update_client_message_sent method is not used, removing.

* Fri Nov 04 2011 Milan Zazrivec <mzazrivec@redhat.com> 5.10.25-1
- 679335 - store osa-dispatcher jabber password in DB

* Fri Oct 21 2011 Milan Zazrivec <mzazrivec@redhat.com> 5.10.24-1
- 679353 - automatically detect system re-registration

* Fri Sep 30 2011 Jan Pazdziora 5.10.23-1
- 689939 - match star in common name.

* Fri Sep 30 2011 Jan Pazdziora 5.10.22-1
- 621531 - move /etc/rhn/default to /usr/share/rhn/config-defaults (osa-
  dispatcher).

* Thu Aug 11 2011 Miroslav Suchý 5.10.21-1
- True and False constants are defined since python 2.4
- do not mask original error by raise in execption

* Thu Jul 21 2011 Jan Pazdziora 5.10.20-1
- Allow osa-dispatcher to read /sys/.../meminfo.

* Thu Jul 21 2011 Jan Pazdziora 5.10.19-1
- Revert "Fedora 15 uses oracledb_port_t instead of oracle_port_t."

* Mon Jul 18 2011 Jan Pazdziora 5.10.18-1
- Fedora 15 uses oracledb_port_t instead of oracle_port_t.

* Fri Jul 15 2011 Miroslav Suchý 5.10.17-1
- optparse is here since python 2.3 - remove optik (msuchy@redhat.com)

* Tue Jun 07 2011 Jan Pazdziora 5.10.16-1
- 705935 - introduce rhnSQL.commit() after the both SELECT statements that seem
  to be the main loop (a.rogge@solvention.de)

* Mon May 02 2011 Jan Pazdziora 5.10.15-1
- Bumping up version to get above the one we backported to Spacewalk 1.4.
- Revert "bump up epoch, and match version of osad with spacewalk version".
- bump up epoch, and match version of osad with spacewalk version
  (msuchy@redhat.com)

* Fri Apr 15 2011 Jan Pazdziora 5.10.12-1
- require python-hashlib only on rhel and rhel <= 5 (mc@suse.de)
- build osad on SUSE (mc@suse.de)
- provide config (mc@suse.de)

* Fri Apr 15 2011 Jan Pazdziora 5.10.11-1
- Address the spacewalk.common.rhnLog and .rhnConfig castling in osa-dispacher.

* Wed Apr 13 2011 Jan Pazdziora 5.10.10-1
- utilize config.getProxySetting() (msuchy@redhat.com)

* Fri Apr 08 2011 Miroslav Suchý 5.10.9-1
- Revert "idn_unicode_to_pune() have to return string" (msuchy@redhat.com)
- update copyright years (msuchy@redhat.com)

* Tue Apr 05 2011 Michael Mraka <michael.mraka@redhat.com> 5.10.8-1
- idn_unicode_to_pune() has to return string

* Wed Mar 30 2011 Miroslav Suchý 5.10.7-1
- utilize config.getServerlURL()
- 683200 - use pune encoding when connecting to jabber

* Wed Mar 30 2011 Jan Pazdziora 5.10.6-1
- no need to support rhel2 (msuchy@redhat.com)
- RHEL 4 is no longer a target version for osa-dispatcher, fixing .spec to
  always build osa-dispatcher-selinux.

* Tue Mar 08 2011 Michael Mraka <michael.mraka@redhat.com> 5.10.5-1
- fixed osad last_message_time update (PG)
- fixed osad next_action_time update (PG)

* Thu Feb 24 2011 Jan Pazdziora 5.10.4-1
- 662593 - let osad initiate presence subscription (mzazrivec@redhat.com)

* Fri Feb 18 2011 Jan Pazdziora 5.10.3-1
- Revert "Revert "get_server_capability() is defined twice in osad and rhncfg,
  merge and move to rhnlib and make it member of rpclib.Server""
  (msuchy@redhat.com)

* Mon Feb 07 2011 Tomas Lestach <tlestach@redhat.com> 5.10.2-1
- do not check port 5222 on the client (tlestach@redhat.com)

* Thu Feb 03 2011 Tomas Lestach <tlestach@redhat.com> 5.10.1-1
- Bumping version to 5.10

* Thu Feb 03 2011 Tomas Lestach <tlestach@redhat.com> 5.9.53-1
- reverting osa-dispatcher selinux policy rules (tlestach@redhat.com)

* Wed Feb 02 2011 Tomas Lestach <tlestach@redhat.com> 5.9.52-1
- pospone osa-dispatcher start, until jabberd is ready (tlestach@redhat.com)

* Tue Feb 01 2011 Tomas Lestach <tlestach@redhat.com> 5.9.51-1
- Revert "get_server_capability() is defined twice in osad and rhncfg, merge
  and move to rhnlib and make it member of rpclib.Server" (tlestach@redhat.com)

* Fri Jan 28 2011 Miroslav Suchý <msuchy@redhat.com> 5.9.50-1
- get_server_capability() is defined twice in osad and rhncfg, merge and move
  to rhnlib and make it member of rpclib.Server

* Mon Jan 17 2011 Jan Pazdziora 5.9.49-1
- Silence InstantClient 11g-related AVCs in osa-dispatcher.
- Silence diagnostics which was causing AVC denials.

* Tue Dec 21 2010 Jan Pazdziora 5.9.48-1
- SQL changes for PostgreSQL support.

* Fri Dec 10 2010 Michael Mraka <michael.mraka@redhat.com> 5.9.47-1
- 661998 - removed looping symlink
- fixed symlink creation

* Wed Nov 24 2010 Michael Mraka <michael.mraka@redhat.com> 5.9.46-1
- removed unused imports

* Thu Nov 18 2010 Lukas Zapletal 5.9.45-1
- 630867 - Allow osa-dispatcher to connect to the PostgreSQL database with
  PostgreSQL backend.

* Tue Nov 02 2010 Jan Pazdziora 5.9.44-1
- Update copyright years in the rest of the repo.

* Fri Oct 29 2010 Jan Pazdziora 5.9.43-1
- removed unused class JabberCallback (michael.mraka@redhat.com)

* Thu Oct 21 2010 Miroslav Suchý <msuchy@redhat.com> 5.9.42-1
- 612581 - spacewalk-backend modules has been migrated to spacewalk namespace

* Tue Oct 12 2010 Lukas Zapletal 5.9.41-1
- Sysdate pgsql fix in osad

* Tue Oct 12 2010 Jan Pazdziora 5.9.40-1
- The osa-dispatcher SELinux module has the Oracle parts optional as well.

* Mon Oct 04 2010 Michael Mraka <michael.mraka@redhat.com> 5.9.39-1
- replaced local copy of compile.py with standard compileall module

* Wed Aug 04 2010 Jan Pazdziora 5.9.38-1
- Allow osa-dispatcher to talk to PostgreSQL.

* Mon Jul 26 2010 Milan Zazrivec <mzazrivec@redhat.com> 5.9.37-1
- 618300 - default_db is no longer needed

* Tue Jul 20 2010 Milan Zazrivec <mzazrivec@redhat.com> 5.9.36-1
- make osa-dispatcher start after jabberd

* Mon Jun 21 2010 Jan Pazdziora 5.9.35-1
- Some spell checking in %%descriptions.
- OSAD stands for Open Source Architecture Daemon.

* Tue May 04 2010 Jan Pazdziora 5.9.34-1
- 575555 - address corecmd_exec_sbin deprecation warning.

* Tue May 04 2010 Jan Pazdziora 5.9.33-1
- 580047 - address AVCs about sqlnet.log when the database is down.

* Mon Apr 19 2010 Michael Mraka <michael.mraka@redhat.com> 5.9.32-1
- do not start osad by default
- require python-haslib only in RHEL5

* Mon Feb 22 2010 Michael Mraka <michael.mraka@redhat.com> 5.9.30-1
- fixed missing Requires: python-hashlib

* Thu Feb 04 2010 Michael Mraka <michael.mraka@redhat.com> 5.9.29-1
- updated copyrights

* Mon Feb 01 2010 Michael Mraka <michael.mraka@redhat.com> 5.9.28-1
- use rhnLockfile.py from rhnlib

* Fri Jan 29 2010 Michael Mraka <michael.mraka@redhat.com> 5.9.27-1
- fixed the sha module is deprecated

* Fri Jan 29 2010 Jan Pazdziora 5.9.26-1
- 559230 - address errors during package removal.
- Do not hide any error messages produced by semanage port -a.

* Wed Jan 27 2010 Miroslav Suchy <msuchy@redhat.com> 5.9.25-1
- replaced popen2 with subprocess in client (michael.mraka@redhat.com)

* Mon Jan 18 2010 Michael Mraka <michael.mraka@redhat.com> 5.9.24-1
- fixed syntax error in init.d scripts

* Fri Jan 15 2010 Michael Mraka <michael.mraka@redhat.com> 5.9.23-1
- implement condrestart for osad init script
- make reload alias for restart
- add osad-auth.conf as normal file with placeholder content

* Tue Oct 27 2009 Miroslav Suchy <msuchy@redhat.com> 5.9.22-1
- Make debugging osa* network/jabber issues easier (joshua.roys@gtri.gatech.edu)

* Tue Aug 04 2009 Jan Pazdziora 5.9.21-1
- 514320 - open the pid file with append

* Mon Jul 27 2009 John Matthews <jmatthew@redhat.com> 5.9.20-1
- 512732 - on Fedora 12, it will be just and corenet_udp_bind_generic_node and
  corenet_udp_bind_all_nodes. (jpazdziora@redhat.com)

* Mon Jul 27 2009 Jan Pazdziora 5.9.19-1
- 512732 - on Fedora 11, corenet_udp_bind_lo_node is no longer available
- Build osa-dispatcher-selinux again

* Thu Jul 23 2009 Devan Goodwin <dgoodwin@redhat.com> 5.9.18-1
- Remove Requires python-optik. (dgoodwin@redhat.com)

* Wed Jul 22 2009 Devan Goodwin <dgoodwin@redhat.com> 5.9.17-1
- Disable osad selinux for Fedora 11. (dgoodwin@redhat.com)

* Mon Jul 20 2009 Devan Goodwin <dgoodwin@redhat.com> 5.9.16-1
- Add osad BuildRequires for python-devel. (dgoodwin@redhat.com)

* Thu Jun 25 2009 John Matthews <jmatthew@redhat.com> 5.9.15-1
- 508064 - fix osad installation errors on client (mzazrivec@redhat.com)

* Thu Jun 18 2009 Jan Pazdziora 5.9.14-1
- 505606 - Require at least selinux-policy 2.4.6-114

* Mon Jun 15 2009 Miroslav Suchy <msuchy@redhat.com> 5.9.13-1
- 498611 - run restorecon in %%posttrans
- 498611 - run "semodule -i" in %%post and restorecon in %%posttrans

* Wed Apr 29 2009 Jan Pazdziora 5.9.11-1
- move the %%post SELinux activation to
  /usr/sbin/osa-dispatcher-selinux-enable

* Fri Mar 27 2009 jesus m. rodriguez <jesusr@redhat.com> 5.9.10-1
- added PYTHON-LICENSES.txt file

* Mon Mar 16 2009 Jan Pazdziora 5.9.9-1
- remove /usr/sbin/semanage: Port tcp/1290 already defined error
- allow osa-dispatcher to use NIS

* Wed Mar 11 2009 jesus m. rodriguez <jesusr@redhat.com> 5.9.8-1
- 479825 - fix osa-dispatcher to start after oracle(-xe) and stop before them.

* Thu Feb 12 2009 Jan Pazdziora 5.9.6-1
- do not build osa-dispatcher-selinux on RHEL 4 and earlier.
- osa-dispatcher-selinux: setsebool is not used, so no need to Require it

* Mon Feb  9 2009 Jan Pazdziora 5.9.5-1
- addressed additional AVC denials of osa-dispatcher

* Wed Feb  4 2009 Miroslav Suchy <msuchy@redhat.com> 5.9.4-1
- 468060 - correctly return status of daemon
- fix some macros
- edit descriptions
- add LICENSE

* Wed Jan 14 2009 Jan Pazdziora 5.9.2-1
- separate package osa-dispatcher-selinux merged in as a subpackage

* Wed Jan 14 2009 Jan Pazdziora
- changes to osa-dispatcher-selinux to allow service osa-dispatcher start
  on RHEL 5.2 to run without any AVC denials except one caused by lookup
  of /root/.rpmmacros

* Mon Jan 12 2009 Jan Pazdziora
- the initial release of osa-dispatcher-selinux
- based on spacewalk-selinux
- which was inspired by Rob Myers' oracle-selinux

* Tue Dec 16 2008 Michael Mraka <michael.mraka@redhat.com> 5.9.1-1
- resolves #474548 - bumped version

* Tue Oct 21 2008 Michael Mraka <michael.mraka@redhat.com> 0.3.2-1
- resolves #467717 - fixed sysvinit scripts

* Wed Sep 24 2008 Milan Zazrivec 0.3.1-1
- bumped version for spacewalk 0.3

* Tue Sep  2 2008 Pradeep Kilambi <pkilambi@redhat.com> 0.2-1
- fix osa-dispatcher to depend on new server package

* Thu Jun 12 2008 Pradeep Kilambi <pkilambi@redhat.com>  - 5.2.0-1
- new build

* Tue Jan  25 2008 Jan Pazdziora - 5.1.0-7
- Resolves #429578, OSAD suspending

* Tue Jan  8 2008 Jan Pazdziora - 5.1.0-6
- Resolves #367031, OSAD daemon hard looping
- Resolves #426201, Osad connects to Satellite at times instead of Proxy

* Thu Oct 18 2007 James Slagle <jslagle@redhat.com> - 5.1.0-4
- Resolves #185476

* Tue Oct 08 2007 Pradeep Kilambi <pkilambi@redhat.com> - 5.1.0-3
- new build

* Tue Sep 25 2007 Pradeep Kilambi <pkilambi@redhat.com> - 5.1.0-2
- get rid of safe-rhn-check and use rhn_check

* Tue Sep 25 2007 Pradeep Kilambi <pkilambi@redhat.com> - 5.1.0-1
- bumping version for consistency

* Thu Apr 12 2007 Pradeep Kilambi <pkilambi@redhat.com> - 0.9.2-1
- adding dist tags

* Thu Oct 05 2006 James Bowes <jbowes@redhat.com> - 0.9.1-2
- Get python version dynamically.

* Wed Sep 20 2006 James Bowes <jbowes@redhat.com> - 0.9.1-1
- Set logrotate to limit the log file to 100M.

* Wed Jun 30 2004 Mihai Ibanescu <misa@redhat.com>
- First build
