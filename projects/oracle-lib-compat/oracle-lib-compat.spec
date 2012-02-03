Name:           oracle-lib-compat
Version:        11.2.0.6
Release:        1%{?dist}
Summary:        Compatibility package so that perl-DBD-Oracle will install
Group:          Applications/Multimedia
License:        GPLv2
# This src.rpm is cannonical upstream
# You can obtain it using this set of commands
# git clone git://git.fedorahosted.org/git/spacewalk.git/
# cd spec-tree/oracle-lib-compat
# make srpm
URL:            https://fedorahosted.org/spacewalk
Source0:	https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-root-%(%{__id_u} -n)

%ifarch s390 s390x
%define icversion 10.2.0.4.0
%define icdir %{icversion}
Requires:       oracle-instantclient-basic = %{icversion}
Requires:       oracle-instantclient-sqlplus = %{icversion}
BuildRequires:       oracle-instantclient-basic = %{icversion}
BuildRequires:       oracle-instantclient-sqlplus = %{icversion}
%define soversion 10
%else
%define icversion 11.2.0.2.0
%define icdir 11.2
Requires:       oracle-instantclient11.2-basic = %{icversion}
Requires:       oracle-instantclient11.2-sqlplus = %{icversion}
BuildRequires:       oracle-instantclient11.2-basic = %{icversion}
BuildRequires:       oracle-instantclient11.2-sqlplus = %{icversion}
%define soversion 11
%endif

%if 0%{?suse_version}
BuildRequires:  prelink
Requires(post): prelink
Requires(post): file
Requires(post): findutils
%else
Requires(post): ldconfig
Requires(post): /usr/bin/execstack
Requires(post): /usr/bin/file
Requires(post): /usr/bin/xargs
%endif

%ifarch x86_64
%define lib64 ()(64bit)
Requires:       libaio.so.1%{lib64}
%endif
Provides:       libocci.so.%{soversion}.1%{?lib64}   = %{icversion}
Provides:       libnnz%{soversion}.so%{?lib64}       = %{icversion}
Provides:       libocijdbc%{soversion}.so%{?lib64}   = %{icversion}
Provides:       libclntsh.so.%{soversion}.1%{?lib64} = %{icversion}
Provides:       libociei.so%{?lib64}       = %{icversion}
Provides:       ojdbc14                    = %{icversion}
Obsoletes:      rhn-oracle-jdbc           <= 1.0
Requires:       libstdc++.so.5%{?lib64}

%description
Compatibility package so that perl-DBD-Oracle will install.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo %{_libdir}/oracle/%{icdir}/client/lib >>$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/oracle-instantclient-%{icdir}.conf

# do not replace /usr/lib with _libdir macro here
# XE server is 32bit even on 64bit platforms
echo /usr/lib/oracle/xe/app/oracle/product/10.2.0/server/lib >>$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/oracle-xe.conf

%ifarch x86_64 s390x

mkdir -p $RPM_BUILD_ROOT%{_libdir}/oracle/%{icdir}
ln -sf ../../../lib/oracle/%{icdir}/client64 $RPM_BUILD_ROOT%{_libdir}/oracle/%{icdir}/client

mkdir -p $RPM_BUILD_ROOT/usr/lib/oracle/%{icdir}/client64/lib/network/admin
echo 'diag_adr_enabled = off' > $RPM_BUILD_ROOT/usr/lib/oracle/%{icdir}/client64/lib/network/admin/sqlnet.ora
%else
mkdir -p $RPM_BUILD_ROOT/usr/lib/oracle/%{icdir}/client/lib/network/admin
echo 'diag_adr_enabled = off' > $RPM_BUILD_ROOT/usr/lib/oracle/%{icdir}/client/lib/network/admin/sqlnet.ora
%endif

%ifnarch s390x
mkdir -p $RPM_BUILD_ROOT/%{_javadir}
%if 0%{?suse_version}
ln -sf ../../lib/oracle/%{icdir}/client64/lib/ojdbc5.jar $RPM_BUILD_ROOT/%{_javadir}/ojdbc14.jar
%else
ln -sf ../../%{_lib}/oracle/%{icdir}/client/lib/ojdbc6.jar $RPM_BUILD_ROOT/%{_javadir}/ojdbc14.jar
%endif
%endif

%if 0%{?rhel} && 0%{?rhel} < 6
%define tomcatname tomcat5
%else
%define tomcatname tomcat6
%endif
install -d $RPM_BUILD_ROOT%{_datadir}/%{tomcatname}/bin
install tomcat-setenv.sh $RPM_BUILD_ROOT%{_datadir}/%{tomcatname}/bin/setenv.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%ifarch x86_64 s390x
%{_libdir}/oracle
%dir /usr/lib/oracle/%{icdir}/client64/lib/network
%dir /usr/lib/oracle/%{icdir}/client64/lib/network/admin
/usr/lib/oracle/%{icdir}/client64/lib/network/admin/sqlnet.ora
%else
%dir /usr/lib/oracle/%{icdir}/client/lib/network
%dir /usr/lib/oracle/%{icdir}/client/lib/network/admin
/usr/lib/oracle/%{icdir}/client/lib/network/admin/sqlnet.ora
%endif
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/oracle-instantclient-%{icdir}.conf
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/oracle-xe.conf
%ifnarch s390x
%{_javadir}/ojdbc14.jar
%endif
%{_datadir}/%{tomcatname}/bin/setenv.sh
%if 0%{?suse_version}
%dir %{_datadir}/%{tomcatname}
%dir %{_datadir}/%{tomcatname}/bin
%endif

%post
ldconfig

# clear execstack on libs in oracle's provided instantclient rpm
find %{_prefix}/lib/oracle/%{icdir} \
        | xargs file | awk -F: '/ELF.*(executable|shared object)/ {print $1}' \
        | xargs execstack -c

%changelog
* Fri Feb 03 2012 Jan Pazdziora 11.2.0.6-1
- Avoid cat: write error: Broken pipe when calling tomcat service under trap ''
  PIPE

* Mon May 16 2011 Jan Pazdziora 11.2.0.5-1
- Both tomcat5 and tomcat6 which needs the LD_PRELOAD set.

* Wed May 04 2011 Jan Pazdziora 11.2.0.4-1
- We unset LD_PRELOAD to force ldd to show the libldap line with => even if
  LD_PRELOAD was already set.

* Mon Jan 17 2011 Jan Pazdziora 11.2.0.3-1
- Set diag_adr_enabled to off.

* Mon Jan 10 2011 Jan Pazdziora 11.2.0.2-1
- On x86_64, require 64bit version of libaio for InstantClient 11g.

* Fri Jan 07 2011 Jan Pazdziora 11.2.0.1-1
- Have separate ld.so.conf.d for InstantClient and for XE server.
- InstantClient 11 contains ojdbc5 and ojdbc6, we will change the target of the
  symlink for now.
- Need to use the "11" in .so Provides as well.
- Switch to Oracle InstantClient 11 in oracle-lib-compat.

* Thu Sep 23 2010 Michael Mraka <michael.mraka@redhat.com> 10.2.0.25-1
- instantclient on s390(x) upgraded to 10.2.0.4
- switched to default VersionTagger

* Thu Sep 23 2010 Jan Pazdziora 10.2-24
- 623115 - file lookup using just the linker name (libldap.so) fails if
  openldap-devel is not installed.

* Mon Sep 13 2010 Jan Pazdziora 10.2-23
- 623115 - force tomcat to use the stock openldap, overriding the ldap_*
  symbols in libclntsh.so*.

* Thu Apr 15 2010 Michael Mraka <michael.mraka@redhat.com> 10.2-22
- fixed errors in %%post

* Wed Sep 09 2009 Michael Mraka <michael.mraka@redhat.com> 10.2-21
- 506951 - clear exec stack on instantclient libs (fixes selinux avc denial)

* Tue Apr 07 2009 Michael Mraka <michael.mraka@redhat.com> 10.2-20
- specified exact version of instantclient

* Mon Mar 02 2009 Devan Goodwin <dgoodwin@redhat.com> 10.2-19
- Version bump to allow fresh dist-cvs tags.

* Mon Dec 15 2008 Michael Mraka <michael.mraka@redhat.com> 10.2-16
- added /usr/bin/sqlplus for 64bit platforms
- added filesystem standard compatible link /usr/lib64/oracle/10.2.0.4/client
- added Requires: libstdc++.so.5 to satisfy instantclient libs
- added Provides: ojdbc14, Obsoletes: rhn-oracle-jdbc
- fixed rpmlint warnings

* Wed Oct 22 2008 Michael Mraka <michael.mraka@redhat.com> 10.2-13
- resolved #461765 - oracle libs not loaded

* Thu Sep 25 2008 Milan Zazrivec 10.2-12
- merged changes from release-0.2 branch
- fixed s390x

* Thu Sep 11 2008 Jesus Rodriguez <jesusr@redhat.com> 10.2-11
- fix x86_64

* Thu Sep  4 2008 Michael Mraka <michael.mraka@redhat.com> 10.2-8
- fixed rpmlint errors and warnings
- built in brew/koji

* Mon Jul 29 2008 Mike McCune <mmccune@redhat.com>
- Removing uneeded Requires compat-libstdc++

* Tue Jul 2 2008 Mike McCune <mmccune@redhat.com>
- Adding ldconfig for the 64bit instantclient libs

* Tue Jul 1 2008 Mike McCune <mmccune@redhat.com>
- relaxing instantclient version requirement to be >= vs =

* Mon Jun 16 2008 Michael Mraka <michael.mraka@redhat.com>
- added 64bit libs macro

* Fri Jun 13 2008 Devan Goodwin <dgoodwin@redhat.com> 10.2-3
- Add symlink for to Oracle 10.2.0.4 libraries.

* Wed Jun 4 2008 Jesus Rodriguez <jmrodri at gmail dot com> 10.2-1
- initial compat rpm

