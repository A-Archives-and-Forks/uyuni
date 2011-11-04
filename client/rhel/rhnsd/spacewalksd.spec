# package renaming fun :(
%define rhn_client_tools spacewalk-client-tools
%define rhn_setup	 spacewalk-client-setup
%define rhn_check	 spacewalk-check
%define rhnsd		 spacewalksd
#
Summary: Spacewalk query daemon
License: GPLv2
Group: System Environment/Base
Source0: https://fedorahosted.org/releases/s/p/spacewalk/rhnsd-%{version}.tar.gz
URL:     https://fedorahosted.org/spacewalk
Name: spacewalksd
Version: 4.9.7
Release: 1%{?dist}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gettext
Provides: rhnsd = %{version}-%{release}
Obsoletes: rhnsd < %{version}-%{release}

Requires: %{rhn_check} >= 0.0.8
%if !0%{?suse_version}
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
%else
Requires(preun): %fillup_prereq %insserv_prereq
%endif

%description
The Red Hat Update Agent that automatically queries the Red Hat
Network servers and determines which packages need to be updated on
your machine, and runs any actions.

%prep
%setup -q

%build
make -f Makefile.rhnsd %{?_smp_mflags} CFLAGS="%{optflags}"

%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?suse_version}
mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
make INIT_DIR=$RPM_BUILD_ROOT/etc/init.d -f Makefile.rhnsd install VERSION=%{version}-%{release} PREFIX=$RPM_BUILD_ROOT MANPATH=%{_mandir}
install -m 0755 rhnsd.init.SUSE $RPM_BUILD_ROOT/%{_initrddir}/rhnsd
rm -f $RPM_BUILD_ROOT/usr/share/locale/no/LC_MESSAGES/rhnsd.mo
%else
make -f Makefile.rhnsd install VERSION=%{version}-%{release} PREFIX=$RPM_BUILD_ROOT MANPATH=%{_mandir}
%endif

# add rclink
ln -sf ../../etc/init.d/rhnsd $RPM_BUILD_ROOT/%{_sbindir}/rcrhnsd

%find_lang rhnsd


%post
%if 0%{?suse_version}
%{fillup_and_insserv rhnsd}
%else
/sbin/chkconfig --add rhnsd
%endif

%preun
%if 0%{?suse_version}
%stop_on_removal rhnsd
exit 0
%else
if [ $1 = 0 ] ; then
    /etc/rc.d/init.d/rhnsd stop >/dev/null 2>&1
    /sbin/chkconfig --del rhnsd
fi
%endif

%postun
%if 0%{?suse_version}
%restart_on_update rhnsd
%{insserv_cleanup}
%else
if [ "$1" -ge "1" ]; then
    /etc/rc.d/init.d/rhnsd condrestart >/dev/null 2>&1 || :
fi
%endif

%clean
rm -fr $RPM_BUILD_ROOT


%files -f rhnsd.lang
%defattr(-,root,root)
%if 0%{?suse_version}
%dir %{_sysconfdir}/sysconfig/rhn
%endif
%{_sbindir}/rcrhnsd
%config(noreplace) %{_sysconfdir}/sysconfig/rhn/rhnsd
%{_sbindir}/rhnsd
%{_initrddir}/rhnsd
%{_mandir}/man8/rhnsd.8*
%doc LICENSE
%if 0%{?suse_version} == 1010
# locale dirs missing in SLE-10 filesystem package:
%dir %{_datadir}/locale/as
%dir %{_datadir}/locale/as/LC_MESSAGES
%dir %{_datadir}/locale/hy
%dir %{_datadir}/locale/hy/LC_MESSAGES
%dir %{_datadir}/locale/my
%dir %{_datadir}/locale/my/LC_MESSAGES
%dir %{_datadir}/locale/or
%dir %{_datadir}/locale/or/LC_MESSAGES
%dir %{_datadir}/locale/si
%dir %{_datadir}/locale/si/LC_MESSAGES
%dir %{_datadir}/locale/ur
%dir %{_datadir}/locale/ur/LC_MESSAGES
%endif

%changelog
* Tue Nov 02 2010 Jan Pazdziora 4.9.7-1
- Update copyright years in the rest of the repo.
- update .po and .pot files for rhnsd

* Thu Aug 12 2010 Milan Zazrivec <mzazrivec@redhat.com> 4.9.6-1
- update .po and .pot files for rhnsd (msuchy@redhat.com)

* Thu Jul 01 2010 Miroslav Suchý <msuchy@redhat.com> 4.9.4-1
- l10n: Updates to Czech (cs) translation (msuchy@fedoraproject.org)
- cleanup - removing translation file, which does not match any language code
  (msuchy@redhat.com)
- update po files for rhnsd (msuchy@redhat.com)
- generate new pot file for rhnsd (msuchy@redhat.com)
- l10n: Updates to Polish (pl) translation (raven@fedoraproject.org)

* Fri Mar 19 2010 Jan Pazdziora 4.9.3-1
- Check return value of regcomp, fix a memory leak (Joshua Roys)

* Wed Feb 10 2010 Miroslav Suchý <msuchy@redhat.com> 4.9.2-1
- Pass version define to the compiler (Jan Pazdziora)
- 533895 - if init script is run user return code 4
- 533891 - if reloading fails return code 7
- 533891 - implement force-reload
- 533867 - init script, wrong parameter should return 2

* Tue Feb 09 2010 Jan Pazdziora 4.9.1-1
- 563173 - change the logging and config processing logic

* Thu Feb 04 2010 Michael Mraka <michael.mraka@redhat.com> 4.8.3-1
- updated copyrights

* Mon Jan 25 2010 Tomas Lestach <tlestach@redhat.com> 4.8.2-1
- fixing systemid parsing (joshua.roys@gtri.gatech.edu)

* Thu Jan 21 2010 Miroslav Suchý <msuchy@redhat.com> 4.8.1-1
- bumping up version, to be ahead of rhel5 versions

* Tue Dec  1 2009 Miroslav Suchý <msuchy@redhat.com> 4.5.16-1
- 502234 - fixing issue where the rhnsd init script would fail to reload the configuration, a forward port of a patch from rhel 4 (jsherril@redhat.com)
- 541682 - make env. for rhn_check consistent with osad (mzazrivec@redhat.com)

* Wed Nov 25 2009 Miroslav Suchý <msuchy@redhat.com> 4.5.15-1
- hardcode MANPATH

* Fri Sep 25 2009 Tomas Lestach <tlestach@redhat.com> 4.5.14-1
- removed hardcoded systemid path (tlestach@redhat.com)

* Tue Sep 22 2009 Miroslav Suchý <msuchy@redhat.com> 4.5.13-1
- use macros
- pass CFLAGS on correct position
- add LICENSE file
- change header info to actual license

* Mon Sep 21 2009 Miroslav Suchý <msuchy@redhat.com> 4.5.12-1
- implement try-restart as alias for condrestart
- add LSB header
- change url, source0 and requires according to packaging guidelines

* Tue Jul 21 2009 John Matthews <jmatthew@redhat.com> 4.5.11-1
- #503719 - fix for postun scriptlet error (pkilambi@redhat.com)

* Tue Jul  7 2009 Pradeep Kilambi <pkilambi@redhat.com>
- Resolves: #503719 - fix for postun scriptlet error

* Thu Jun 25 2009 John Matthews <jmatthew@redhat.com> 4.5.10-1
- 243699: fixing the error code when unknown command is used with rhnsd init
  (pkilambi@redhat.com)
- updateing translations for rhnsd (pkilambi@redhat.com)

* Wed Jun  3 2009 Pradeep Kilambi <pkilambi@redhat.com> 4.7.0-3
- Resolves:  #243699 -fixing error code for unknown command to rhnsd init script

* Mon May 11 2009 Pradeep Kilambi <pkilambi@redhat.com> 4.7.0-2
- Updated translations.
- Resolves:  #243699

* Tue Jan 27 2009 Miroslav Suchý <msuchy@redhat.com> 4.5.9-1
- rebuild

* Wed Jan 21 2009 Pradeep Kilambi <pkilambi@redhat.com> 4.5.8-1
- Remove usage of version and sources files.

* Mon Dec 11 2006 James Bowes <jbowes@redhat.com> - 4.5.7-1
- Updated translations.
- Related: #216837

* Fri Dec 01 2006 James Bowes <jbowes@redhat.com> - 4.5.6-1
- Updated translations.

* Thu Nov 30 2006 James Bowes <jbowes@redhat.com> - 4.5.5-1
- New and updated translations.

* Tue Nov 28 2006 James Bowes <jbowes@redhat.com> - 4.5.4-1
- New and updated translations.

* Tue Nov 14 2006 James Bowes <jbowes@redhat.com> - 4.5.3-1
- Updated manual page.
- Require gettext.

* Mon Oct 30 2006 James Bowes <jbowes@redhat.com> - 4.5.2-1
- New and updated translations.

* Thu Sep 14 2006 James Bowes <jbowes@redhat.com> - 4.5.1-1
- Fix for bz 163483: rhnsd spawns children with SIGPIPE set to SIG_IGN

* Fri Jul 21 2006 James Bowes <jbowes@redhat.com> - 4.5.0-3
- Require rhn-check, not rhn_check.

* Wed Jul 19 2006 James Bowes <jbowes@redhat.com> - 4.5.0-2
- spec file cleanups.

* Fri Jul 07 2006 James Bowes <jbowes@redhat.com> - 4.5.0-1
- Release for RHEL5 matching with up2date.

* Thu May 18 2006 James Bowes <jbowes@redhat.com> - 0.0.2-1
- Refer to the proper commands in the man page.

* Tue Apr 11 2006 James Bowes <jbowes@redhat.com> - 0.0.1-1
- initial split from main up2date package.
