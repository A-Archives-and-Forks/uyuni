
%define heriloom_pkgtools_version 070227

Name:		heirloom-pkgtools
Summary:	Heirloom Packaging Tools
Group:		Development/Tools
License:	CDDL
Version:	1.%{heriloom_pkgtools_version}
Release:	9%{?dist}

URL:		http://heirloom.sourceforge.net/pkgtools.html
Source0:	%{name}-%{heriloom_pkgtools_version}.tar.bz2
Patch1:		getpass.c.patch
Patch2:		scriptvfy.l.patch
Patch3:		binpath.patch
Patch4:		sbinpath.patch
Patch5:		cpio-D.patch
Patch6:		compute_checksum-64bit.patch
Patch7:		use-flex.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc
BuildRequires:	openssl-devel
BuildRequires:	flex
%if 0%{?fedora}
BuildRequires:	compat-flex = 2.5.4a
%endif

%description
Heirloom Packaging Tools are Linux ports of the SVR4
application packaging tools, as released by Sun as part of
OpenSolaris.

%prep
%setup -q -n %{name}-%{heriloom_pkgtools_version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%if 0%{?fedora}
%patch7 -p1
%endif

%build
make -f makefile SHELL=/bin/bash CC=gcc BINDIR=%{_bindir} SBINDIR=%{_sbindir}

%install
rm -rf $RPM_BUILD_ROOT
make -f makefile install SHELL=/bin/bash INSTALL=/usr/bin/install ROOT=$RPM_BUILD_ROOT BINDIR=%{_bindir} SBINDIR=%{_sbindir} MANDIR=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%config %_sysconfdir/device.tab
%{_sbindir}/installf
%{_sbindir}/pkgadd
%{_sbindir}/pkgask
%{_sbindir}/pkgchk
%{_sbindir}/pkgrm
%{_sbindir}/removef
%{_bindir}/pkginfo
%{_bindir}/pkgmk
%{_bindir}/pkgparam
%{_bindir}/pkgproto
%{_bindir}/pkgtrans
%dir %{_usr}/sadm
%dir %{_usr}/sadm/install
%dir %{_usr}/sadm/install/bin
%dir %{_usr}/sadm/install/scripts
%{_usr}/sadm/install/bin/pkginstall
%{_usr}/sadm/install/bin/pkgname
%{_usr}/sadm/install/bin/pkgremove
%{_usr}/sadm/install/scripts/cmdexec
%{_usr}/sadm/install/scripts/i.CompCpio
%{_usr}/sadm/install/scripts/i.awk
%{_usr}/sadm/install/scripts/i.build
%{_usr}/sadm/install/scripts/i.sed
%{_usr}/sadm/install/scripts/r.awk
%{_usr}/sadm/install/scripts/r.build
%{_usr}/sadm/install/scripts/r.sed
%{_mandir}/man1/pkginfo.1.gz
%{_mandir}/man1/pkgmk.1.gz
%{_mandir}/man1/pkgparam.1.gz
%{_mandir}/man1/pkgproto.1.gz
%{_mandir}/man1/pkgtrans.1.gz
%dir %{_mandir}/man1m
%{_mandir}/man1m/installf.1m.gz
%{_mandir}/man1m/pkgadd.1m.gz
%{_mandir}/man1m/pkgask.1m.gz
%{_mandir}/man1m/pkgchk.1m.gz
%{_mandir}/man1m/pkgrm.1m.gz
%{_mandir}/man1m/removef.1m.gz
%{_mandir}/man5/depend.5.gz
%{_mandir}/man5/pkginfo.5.gz
%{_mandir}/man5/pkgmap.5.gz
%{_mandir}/man5/prototype.5.gz
%dir %{_var}/sadm
%dir %{_var}/sadm/install
%dir %{_var}/sadm/install/admin
%{_var}/sadm/install/admin/default

%changelog
* Tue Dec 11 2012 Jan Pazdziora 1.070227-9
- Walk both 32bit and 64bit paths.

* Tue Dec 11 2012 Jan Pazdziora 1.070227-8
- On Fedoras, use compat-flex and -lfl.

* Tue Dec 11 2012 Jan Pazdziora 1.070227-7
- set correct tagger for heirloom-pkgtools
- set correct builder for heirloom-pkgtools

* Fri Feb 27 2009 Jan Pazdziora 1.070227-6
- fixed pkgmk producing wrong checksums in pkgmap on 64bit

* Wed Dec 31 2008 Jan Pazdziora
- stripped the D option from cpio commands

* Sat Dec 27 2008 Jan Pazdziora
- add patch getpass.c.patch, removing stropts.h #include
- define a couple of needed things, like yytchar, in scriptvfy.l
- changing the use of BINDIR to /bin for system commands
- changing the use /sbin to /bin for multiple system commands

* Fri Dec 12 2008 Jan Pazdziora
- initial rpm release

