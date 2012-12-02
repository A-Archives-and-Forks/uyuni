Name:         perl-NOCpulse-Utils
Version:      1.14.11.1
Release:      1%{?dist}
Summary:      NOCpulse utility packages
URL:          https://fedorahosted.org/spacewalk
Source0:      https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
BuildArch:    noarch
Group:        Development/Libraries
License:      GPLv2
Buildroot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if 0%{?suse_version}
BuildRequires: nocpulse-common
%else
Requires:     perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%endif

%description
NOCpulse provides application, network, systems and transaction monitoring,
coupled with a comprehensive reporting system including availability,
historical and trending reports in an easy-to-use browser interface.

This package provides miscellaneous utility modules.

%prep
%setup -q

%build
# Nothing to build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Utils/test

install -m 444 Module.pm          $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Module.pm 
#install -m 444 TestRunner.pm      $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Utils/TestRunner.pm
install -m 444 Error.pm           $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Utils/Error.pm
#install -m 755 -D runtest.pl      $RPM_BUILD_ROOT/%{_bindir}/runtest.pl
install -m 444 XML.pm          $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Utils/XML.pm
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3/
/usr/bin/pod2man $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Module.pm |gzip > $RPM_BUILD_ROOT%{_mandir}/man3/NOCpulse::Module.3pm.gz

%files 
%dir %{perl_vendorlib}/NOCpulse
%{perl_vendorlib}/NOCpulse/*
%{_mandir}/man3/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jan  7 2009 Milan Zazrivec 1.14.11-1
- include documentation fixes

* Wed Dec  3 2008 Miroslav Suchý <msuchy@redhat.com> 1.14.10-1
- changed Source0 to point to fedorahosted.org

* Mon Oct 20 2008 Miroslav Suchý <msuchy@redhat.com> 1.14.9-1
- 467441 - fix namespace

* Mon Oct 20 2008 Miroslav Suchy <msuchy@redhat.com> 1.14.8-1
- 467443 - fix typo in module name

* Tue Oct 14 2008 Miroslav Suchy <msuchy@redhat.com> 1.14.7-1
- remove nocpulse-common from requires

* Thu Aug 20 2008 Miroslav Suchy <msuchy@redhat.com> 1.14.5-1
- edit spec to comply with Fedora guidelines

* Thu Jun 19 2008 Miroslav Suchy <msuchy@redhat.com>
- migrating nocpulse home dir (BZ 202614)

* Wed Jun  4 2008 Milan Zazrivec <mzazrivec@redhat.com> 1.14.2-9
- fixed file permissions

* Tue May 27 2008 Jan Pazdziora 1.14.2-8
- fixed bugzilla 438770
u rebuild in dist.cvs

