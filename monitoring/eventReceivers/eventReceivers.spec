Name:         eventReceivers
Source0:      https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
Version:      2.20.15
Release:      1%{?dist}
Summary:      Command Center Event Receivers
URL:          https://fedorahosted.org/spacewalk
BuildArch:    noarch
Group:        Applications/Internet
License:      GPLv2
Buildroot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if 0%{?suse_version}
Requires:     perl = %{perl_version}
%else
Requires:     perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%endif

# smtpdaemon or mailx. I picked up smtpdaemon
%if 0%{?suse_version}
Requires:     smtp_daemon
%else
Requires:     smtpdaemon
%endif

%description
NOCpulse provides application, network, systems and transaction monitoring,
coupled with a comprehensive reporting system including availability,
historical and trending reports in an easy-to-use browser interface.

This package contains handler, which receive events from scouts.

%prep
%setup -q

%build
#Nothing to build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse
install -m644 *.pm $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse

%{_fixperms} $RPM_BUILD_ROOT/*

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%doc LICENSE

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Oct 13 2010 Jan Pazdziora 2.20.15-1
- 484612 - correctly set From using Mail::Send (msuchy@redhat.com)

* Wed Mar 31 2010 Miroslav Suchý <msuchy@redhat.com> 2.20.14-1
- do not care about sending email, transfer the worries to perl-MailTools
- 569745 - send email using address set in targetEmail

* Mon May 11 2009 Miroslav Suchý <msuchy@redhat.com> 2.20.13-1
- 499568 - correctly detect if we are sub-request

* Fri Apr 17 2009 Devan Goodwin <dgoodwin@redhat.com> 2.20.12-1
- Adding use Apache2::RequestRec for $r->main. (jpazdziora@redhat.com)

* Tue Feb 24 2009 Miroslav Suchý <msuchy@redhat.com> 2.20.11-1
- add LICENSE
- add Requires smtpdaemon

* Wed Feb 11 2009 Miroslav Suchý <msuchy@redhat.com> 2.20.10-1
- remove dead code (apachereg)

* Fri Sep 12 2008 Miroslav Suchy <msuchy@redhat.com> 2.20.9-1
- spec cleanup for Fedora

* Fri Jun  6 2008 Milan Zazrivec <mzazrivec@redhat.com> 2.20.8-11
- cvs.dist import
