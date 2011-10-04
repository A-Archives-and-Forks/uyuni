%if  0%{?suse_version}
%define version_major 1.2
%define wwwdocroot /srv/www/htdocs
%define apacheconfdir %{_sysconfdir}/apache2/conf.d
%else
%define wwwdocroot %{_var}/www/html
%define apacheconfdir %{_sysconfdir}/httpd/conf.d
%endif
Name:       spacewalk-branding
Version:    1.6.4
Release:    1%{?dist}
Summary:    Spacewalk branding data

Group:      Applications/Internet
License:    GPLv2
URL:        https://fedorahosted.org/spacewalk/
Source0:    https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildArch:  noarch

BuildRequires: java-devel >= 1.5.0
Requires:   httpd
BuildRequires:   httpd

%description
Spacewalk specific branding, CSS, and images.

%prep
%setup -q

%build
%if  0%{?suse_version}
%define javac javac -target 1.5
%else
%define javac javac
%endif
%javac java/code/src/com/redhat/rhn/branding/strings/StringPackage.java
rm -f java/code/src/com/redhat/rhn/branding/strings/StringPackage.java
jar -cf java-branding.jar -C java/code/src com

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{apacheconfdir}
install -p -m 644 zz-spacewalk-branding.conf %{buildroot}%{apacheconfdir}
install -d -m 755 %{buildroot}/%{wwwdocroot}
install -d -m 755 %{buildroot}/%{wwwdocroot}/nav
install -d -m 755 %{buildroot}%{_datadir}/spacewalk
install -d -m 755 %{buildroot}%{_datadir}/rhn/lib/
%if  0%{?rhel} && 0%{?rhel} < 6
install -d -m 755 %{buildroot}%{_var}/lib/tomcat5/webapps/rhn/WEB-INF/lib/
%else
install -d -m 755 %{buildroot}%{_var}/lib/tomcat6/webapps/rhn/WEB-INF/lib/
%endif
install -d -m 755 %{buildroot}/%{_sysconfdir}/rhn
install -d -m 755 %{buildroot}/%{_prefix}/share/rhn/config-defaults
cp -pR css %{buildroot}/%{wwwdocroot}/
cp -pR img %{buildroot}/%{wwwdocroot}/
cp -pR fonts %{buildroot}/%{wwwdocroot}/
# Appplication expects two favicon's for some reason, copy it so there's just
# one in source:
cp -p img/favicon.ico %{buildroot}/%{wwwdocroot}/
cp -pR templates %{buildroot}/%{wwwdocroot}/
cp -pR styles %{buildroot}/%{wwwdocroot}/nav/
cp -pR setup  %{buildroot}%{_datadir}/spacewalk/
cp -pR java-branding.jar %{buildroot}%{_datadir}/rhn/lib/
%if  0%{?rhel} && 0%{?rhel} < 6
ln -s %{_datadir}/rhn/lib/java-branding.jar %{buildroot}%{_var}/lib/tomcat5/webapps/rhn/WEB-INF/lib/java-branding.jar
%else
ln -s %{_datadir}/rhn/lib/java-branding.jar %{buildroot}%{_var}/lib/tomcat6/webapps/rhn/WEB-INF/lib/java-branding.jar
%endif

%if  0%{?suse_version}
cat > %{buildroot}/%{_prefix}/share/rhn/config-defaults/rhn_docs.conf <<-ENDOFCONFIG
docs.quick_start=/rhn/help/quick/index.jsp
docs.proxy_guide=/rhn/help/proxy-quick/index.jsp
docs.reference_guide=/rhn/help/reference/index.jsp
docs.install_guide=/rhn/help/install/index.jsp
docs.client_config_guide=/rhn/help/client-config/index.jsp
docs.channel_mgmt_guide=http://www.novell.com/documentation/suse_manager/
docs.release_notes=/rhn/help/release-notes/manager/en-US/index.jsp
docs.proxy_release_notes=http://www.novell.com/linux/releasenotes/%{_arch}/SUSE-MANAGER/%{version_major}/
ENDOFCONFIG
%else
cp -p conf/rhn_docs.conf %{buildroot}/%{_prefix}/share/rhn/config-defaults/rhn_docs.conf
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir /%{wwwdocroot}/css
/%{wwwdocroot}/css/*
%dir /%{wwwdocroot}/img
/%{wwwdocroot}/img/*
/%{wwwdocroot}/favicon.ico
%dir /%{wwwdocroot}/fonts
/%{wwwdocroot}/fonts/*
%dir /%{wwwdocroot}/templates
/%{wwwdocroot}/templates/*
%dir /%{wwwdocroot}/nav/styles
/%{wwwdocroot}/nav/styles/*
%config(noreplace) %{apacheconfdir}/zz-spacewalk-branding.conf
%{_datadir}/spacewalk/
%{_datadir}/rhn/lib/java-branding.jar
%if  0%{?rhel} && 0%{?rhel} < 6
%{_var}/lib/tomcat5/webapps/rhn/WEB-INF/lib/java-branding.jar
%else
%{_var}/lib/tomcat6/webapps/rhn/WEB-INF/lib/java-branding.jar
%endif
%{_prefix}/share/rhn/config-defaults/rhn_docs.conf
%dir %{_prefix}/share/rhn/config-defaults
%dir %{wwwdocroot}/nav
%dir /usr/share/rhn
%dir /usr/share/rhn/lib
%dir /var/lib/tomcat6
%dir /var/lib/tomcat6/webapps
%dir /var/lib/tomcat6/webapps/rhn
%dir /var/lib/tomcat6/webapps/rhn/WEB-INF
%dir /var/lib/tomcat6/webapps/rhn/WEB-INF/lib

%doc LICENSE

%changelog
* Fri Sep 30 2011 Jan Pazdziora 1.6.4-1
- 621531 - move /etc/rhn/default to /usr/share/rhn/config-defaults (branding).

* Fri Sep 02 2011 Jan Pazdziora 1.6.3-1
- 558972 - making the navigational bar nice on 2000+ px wide screens.

* Fri Aug 05 2011 Jan Pazdziora 1.6.2-1
- 458413 - hide the bubble help links since we do not ship the documentation
  with Spacewalk.

* Fri Jul 22 2011 Jan Pazdziora 1.6.1-1
- cleanup: revhistory style is not used (msuchy@redhat.com)
- fix typos in css (msuchy@redhat.com)

* Tue Jun 21 2011 Jan Pazdziora 1.5.2-1
- 708957 - remove RHN Satellite Proxy Release Notes link (tlestach@redhat.com)

* Tue May 10 2011 Jan Pazdziora 1.5.1-1
- 484895 - Point the release notes dispatcher to fedorahosted.org.

* Wed Mar 30 2011 Jan Pazdziora 1.4.3-1
- update copyright years (msuchy@redhat.com)
- implement common access keys (msuchy@redhat.com)

* Fri Feb 18 2011 Jan Pazdziora 1.4.2-1
- The LOGGED IN and SIGN OUT are not images since Satellite 5.0 (rhn-360.css),
  removing.

* Wed Feb 09 2011 Michael Mraka <michael.mraka@redhat.com> 1.4.1-1
- made system legend of the same width as side navigation

* Fri Dec 17 2010 Michael Mraka <michael.mraka@redhat.com> 1.3.2-1
- let import PXT modules on fly

* Thu Nov 25 2010 Miroslav Suchý <msuchy@redhat.com> 1.3.1-1
- add GPLv2 license (msuchy@redhat.com)
- cleanup spec (msuchy@redhat.com)
- remove .htaccess file (msuchy@redhat.com)
- point to url where we store tar.gz (msuchy@redhat.com)
- Bumping package versions for 1.3. (jpazdziora@redhat.com)

* Mon Sep 27 2010 Miroslav Suchý <msuchy@redhat.com> 1.2.2-1
- 627920 - Added a larger config file icon for symlinks. Thanks to Joshua Roys
  (paji@redhat.com)

* Wed Sep 01 2010 Jan Pazdziora 1.2.1-1
- 567885 - "Spacewalk release 0.9" leads to 404 (coec@war.coesta.com)

* Mon May 31 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.2-1
- Adding the correct checkstyle for inactive systems
- Added the dupe compare css and javascript magic
- 572714 - fixing css issues with docs

* Mon Apr 19 2010 Michael Mraka <michael.mraka@redhat.com> 1.1.1-1
- bumping spec files to 1.1 packages

* Wed Mar 24 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.4-1
- resigning spacewalk cert
- 516048 - syncing java stack with perl stack on channel naming convention

* Mon Mar 08 2010 Michael Mraka <michael.mraka@redhat.com> 0.9.3-1
- 486430 - changed organization name in default cert

* Thu Feb 11 2010 Justin Sherrill <jsherril@redhat.com> 0.9.2-1
- updating branding package for tomcat6 (jsherril@redhat.com)
- let's start Spacewalk 0.9 (michael.mraka@redhat.com)

* Fri Jan 29 2010 Miroslav Suchý <msuchy@redhat.com> 0.8.2-1
- upadating spacewalk cert (jsherril@redhat.com)

* Fri Jan 08 2010 Jan Pazdziora 0.8.1-1
- Update copyright years to end with 2010.
- Dead code removal.
- bumping Version to 0.8.0 (msuchy@redhat.com)

* Wed Sep 02 2009 Michael Mraka <michael.mraka@redhat.com> 0.7.1-1
- Add symlink capability to config management (joshua.roys@gtri.gatech.edu)
- add the Chat graphic as an advertisement to the layouts
- allow users to chat with spacewalk members on IRC via the web

* Tue Jul 21 2009 John Matthews <jmatthew@redhat.com> 0.6.8-1
- 510146 - Update copyright years from 2002-08 to 2002-09.
  (dgoodwin@redhat.com)

* Tue Jun 30 2009 Miroslav Suchy <msuchy@redhat.com> 0.6.7-1
- 508710 - make bar on top of page wider, so we do not get empty space on wider displays

* Thu Jun 25 2009 John Matthews <jmatthew@redhat.com> 0.6.6-1
- 506489 - remove the link associated with the org name present in the UI
  header (bbuckingham@redhat.com)
- 505101 - update css so that links are underlined when hovering
  (bbuckingham@redhat.com)
- fix to shwo the correct error message css (paji@redhat.com)

* Wed May 27 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.5-1
- 500806 - limit a:hover to links only, changed to a:link:hover (jesusr@redhat.com)

* Thu May 21 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.4-1
- 501038 - Update css to mitigate wrapping of long org names. (jortel@redhat.com)

* Wed May 06 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.3-1
- 444221 - More fixes related to snippet pages in general (paji@redhat.com)
- 484962 - Cleanup System Overview alerts. (dgoodwin@redhat.com)
- 480011 - Added organization to the top header near the username (jason.dobies@redhat.com)

* Mon Apr 20 2009 jesus m. rodriguez <jesusr@redhat.com> 0.6.2-1
- 496321 - add Documentation as a search option on perl pages (jesusr@redhat.com)

* Wed Apr 15 2009 Devan Goodwin <dgoodwin@redhat.com> 0.6.1-1
- 494475,460136 - remove faq & feedback code which used customer service emails.
  (jesusr@redhat.com)
- 443132 - Converted action lists to new list tag. (jsherril@redhat.com)

* Thu Mar 26 2009 jesus m. rodriguez <jesusr@redhat.com> 0.5.8-1
- removing satellite-debug link

* Wed Feb 18 2009 Brad Buckingham <bbuckingham@redhat.com> 0.5.7-1
- adding rhn_docs.conf to enable configurable docs location

* Wed Feb 04 2009 Devan Goodwin <dgoodwin@redhat.com> 0.5.5-1
- Add /var/www/html/favicon.ico.

* Fri Jan 30 2009 Mike McCune <mmccune@gmail.com> 0.5.4-1
- going back to just spacewalk-branding but removing requires: spacewalk-html

* Wed Jan 28 2009 Mike McCune <mmccune@gmail.com> 0.5.3-1
- split out branding jar into its own subpackage.

* Wed Jan 21 2009 Michael Mraka <michael.mraka@redhat.com> 0.5.1-1
- modified branding according to jsp layout changes

* Mon Dec 22 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.1-1
- added spacewalk-public.cert and spacewalk-cert.conf

* Thu Oct 23 2008 Jesus M. Rodriguez <jesusr@redhat.com> 0.1.6-1
- fix square corner on left tab.

* Fri Aug 29 2008 Jesus M. Rodriguez <jesusr@redhat.com> 0.1.5-1
- bz: 460313  css fix for search bar in top right header.

* Tue Aug 12 2008 Devan Goodwin 0.1.4-0
- Adding nav styles.

* Thu Aug 07 2008 Devan Goodwin 0.1.3-0
- Adding templates.

* Wed Aug  6 2008 Jan Pazdziora 0.1.2-0
- decrease version to 0.1.*
- tag for rebuild

* Mon Aug 04 2008  Miroslav Suchy <msuchy@redhat.com>
- fix dependecies, requires spacewalk-html
- bump version

* Wed Jul 30 2008  Devan Goodwin <dgoodwin@redhat.com> 0.2-2
- Adding images.

* Tue Jul 29 2008  Devan Goodwin <dgoodwin@redhat.com> 0.2-1
- Initial packaging.

