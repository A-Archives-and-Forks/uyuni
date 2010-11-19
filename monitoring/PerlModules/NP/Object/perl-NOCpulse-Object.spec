Name:         perl-NOCpulse-Object
Version:      1.26.12
Release:      1%{?dist}%{?suse_version:%{?!dist:.A}.<RELEASE>}
Summary:      NOCpulse Object abstraction for Perl
URL:          https://fedorahosted.org/spacewalk
Source0:      https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
BuildArch:    noarch
%if ! 0%{?suse_version}
Requires:     perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%else
Requires:     perl-Config-IniFiles perl-FreezeThaw
%endif
BuildRequires: perl(Config::IniFiles) perl(FreezeThaw) perl(NOCpulse::Debug) perl(ExtUtils::MakeMaker)
Group:        Development/Libraries
License:      GPLv2
Buildroot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
NOCpulse provides application, network, systems and transaction monitoring,
coupled with a comprehensive reporting system including availability,
historical and trending reports in an easy-to-use browser interface.

This package contain an abstract PERL class that tries and fails to cover up
the ugliness that is OO in Perl, amongst other things.

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{perl_vendorlib}/NOCpulse
%{perl_vendorlib}/NOCpulse/*
%{_mandir}/man3/*
%doc LICENSE

%changelog
* Thu Aug 26 2010 Shannon Hughes <shughes@redhat.com> 1.26.12-1
- Automatic commit of package [perl-NOCpulse-Object] release [1.26.11-1].
  (shughes@redhat.com)

* Thu Aug 26 2010 Shannon Hughes <shughes@redhat.com> 1.26.11-1
-

* Wed Feb 18 2009 Miroslav Suchý <msuchy@redhat.com> 1.26.10-1
- 485893 - add GPL headers to modules

* Tue Feb 17 2009 Miroslav Suchý <msuchy@redhat.com> 1.26.9-1
- add LICENSE
- own NOCpulse dir
- remove optimize flags

* Wed Jan 28 2009 Dennis Gilmore <dennis@ausil.us> 1.26.8-1
- BR perl(ExtUtils::MakeMaker)

* Tue Oct 21 2008 Miroslav Suchý <msuchy@redhat.com> 1.26.7-1
- 467441 - fix namespace

* Tue Sep  2 2008 Miroslav Suchý <msuchy@redhat.com> 1.26.5-1
- edit spec to comply with Fedora Guidelines

* Thu May 29 2008 Jan Pazdziora 1.26.4-7
- rebuild in dist.cvs

