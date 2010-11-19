Name:         NOCpulsePlugins
Version:      2.209.1
Release:      1%{?dist}
Summary:      NOCpulse authored Plug-ins
URL:          https://fedorahosted.org/spacewalk
Source0:      https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
BuildArch:    noarch
%if 0%{?suse_version}
Requires:     perl = %{perl_version}
%else
Requires:     perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%endif
Requires:     nocpulse-common
Group:        Development/Libraries
License:      GPLv2
Buildroot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
NOCpulse provides application, network, systems and transaction monitoring,
coupled with a comprehensive reporting system including availability,
historical and trending reports in an easy-to-use browser interface.

This package contain NOCpulse authored plug-ins for probes.

%package Oracle
Summary:      NOCpulse plug-ins for Oracle
Group:        Development/Libraries
Requires:     %{name} = %{version}

%description Oracle
NOCpulse provides application, network, systems and transaction monitoring,
coupled with a comprehensive reporting system including availability,
historical and trending reports in an easy-to-use browser interface.

This package contain NOCpulse authored plug-ins for Oracle probes.

%prep
%setup -q

%build
# Nothing to build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/nocpulse
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/nocpulse/libexec
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/nocpulse/ProbeState

install -p -m 644 *.ini   $RPM_BUILD_ROOT%{_sysconfdir}/nocpulse
install -p -m 644 *.pm    $RPM_BUILD_ROOT%{_var}/lib/nocpulse/libexec
install -p -m 755 rhn-probe-status $RPM_BUILD_ROOT%{_bindir}
install -p -m 755 rhn-catalog $RPM_BUILD_ROOT%{_bindir}
install -p -m 755 setTrending $RPM_BUILD_ROOT%{_bindir}

for pkg in Apache Apache/test General LogAgent MySQL NetworkService Oracle Oracle/test Satellite Unix Unix/test Weblogic 
do
  fulldir=$RPM_BUILD_ROOT%{_var}/lib/nocpulse/libexec/$pkg
  mkdir -p  $fulldir
  install -p -m 644 $pkg/*.pm $fulldir
done

%post
if [ $1 -eq 2 ]; then
  ls /home/nocpulse/var/ProbeState/* 2>/dev/null | xargs -I file mv file %{_var}/lib/nocpulse/ProbeState
fi

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/nocpulse
%dir %attr(-, nocpulse,nocpulse) %{_var}/lib/nocpulse
%attr(-,nocpulse,nocpulse) %dir %{_var}/lib/nocpulse/ProbeState
%dir %attr(-, nocpulse,nocpulse) %{_var}/lib/nocpulse/libexec
%{_var}/lib/nocpulse/libexec/Apache*
%{_var}/lib/nocpulse/libexec/General*
%{_var}/lib/nocpulse/libexec/LogAgent*
%{_var}/lib/nocpulse/libexec/MySQL*
%{_var}/lib/nocpulse/libexec/NetworkService*
%{_var}/lib/nocpulse/libexec/Satellite*
%{_var}/lib/nocpulse/libexec/Unix*
%{_var}/lib/nocpulse/libexec/Weblogic*
%{_var}/lib/nocpulse/libexec/*.pm
%config %{_sysconfdir}/nocpulse/*
%{_bindir}/*

%files Oracle
%defattr(-,root,root,-)
%{_var}/lib/nocpulse/libexec/Oracle*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Jul 12 2010 Miroslav Suchý <msuchy@redhat.com> 2.209.1-1
- rename status to rhn-probe-status (msuchy@redhat.com)
- rename catalog to rhn-catalog (msuchy@redhat.com)
- fix spelling error (msuchy@redhat.com)
- fix rpmlint warning (msuchy@redhat.com)
- fix spelling error (msuchy@redhat.com)
- put status and catalog to /usr/bin rather then to /var/lib/nocpulse/libexec
  and setting up symlink (msuchy@redhat.com)
- preserve timestamp and set correct attributes for files (msuchy@redhat.com)
- split package NOCpulsePlugins to NOCpulsePlugins-Oracle, which contain Oracle
  only probes (msuchy@redhat.com)
* Wed Jun 10 2009 Miroslav Suchy <msuchy@redhat.com> 2.208.10-1
- 502595 - use ip instead of hostname

* Tue May 26 2009 Miroslav Suchý <msuchy@redhat.com> 2.208.9-1
- 474279 - rewrite TNSping probe (take 2)

* Mon May 11 2009 Milan Zazrivec <mzazrivec@redhat.com> 2.208.7-1
- 498257 - migrate existing files into new nocpulse homedir

* Thu Apr 16 2009 Tomas Lestach <tlestach@redhat.com> 2.208.6-1
- 449919 - fixing SNMP uptime information

* Thu Feb  5 2009 Miroslav Suchý <msuchy@redhat.com> 2.208.5-1
- 474279 - rewrite TNSping probe

* Tue Feb  3 2009 Miroslav Suchý <msuchy@redhat.com> 2.208.4-1
- fix permission of /var/lib/nocpulse/ProbeState

* Thu Dec  4 2008 Miroslav Suchý <msuchy@redhat.com> 2.208.3-1
- fix permission of /var/lib/nocpulse

* Mon Oct 20 2008 Miroslav Suchý <msuchy@redhat.com> 2.208.2-1
- 467441 - fix namespace

* Wed Sep 10 2008 Miroslav Suchý <msuchy@redhat.com> 2.208.1-1
- spec cleanup for Fedora
- remove /opt directory

* Thu Jun 19 2008 Miroslav Suchy <msuchy@redhat.com>
- migrating nocpulse home dir (BZ 202614)

* Fri Jun  6 2008 Milan Zazrivec <mzazrivec@redhat.com> 2.208.0-30
- cvs.dist import
