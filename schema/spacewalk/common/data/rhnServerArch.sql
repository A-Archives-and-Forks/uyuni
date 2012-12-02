--
-- Copyright (c) 2008--2012 Red Hat, Inc.
--
-- This software is licensed to you under the GNU General Public License,
-- version 2 (GPLv2). There is NO WARRANTY for this software, express or
-- implied, including the implied warranties of MERCHANTABILITY or FITNESS
-- FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
-- along with this software; if not, see
-- http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
-- 
-- Red Hat trademarks are not licensed under GPLv2. No permission is
-- granted to use or replicate Red Hat trademarks that are incorporated
-- in this software or its documentation. 
--
--

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'i386-redhat-linux', 'i386', lookup_arch_type('rpm'));
insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'i386-debian-linux', 'i386 Debian', lookup_arch_type('deb'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'i486-redhat-linux', 'i486', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'i586-redhat-linux', 'i586', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'i686-redhat-linux', 'i686', lookup_arch_type('rpm'));


insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'athlon-redhat-linux', 'athlon', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'alpha-redhat-linux', 'alpha', lookup_arch_type('rpm'));
insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'alpha-debian-linux', 'alpha Debian', lookup_arch_type('deb'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'alphaev6-redhat-linux', 'alphaev6', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'ia64-redhat-linux', 'ia64', lookup_arch_type('rpm'));
insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'ia64-debian-linux', 'ia64 Debian', lookup_arch_type('deb'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'sparc-redhat-linux', 'sparc', lookup_arch_type('rpm'));
insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'sparc-debian-linux', 'sparc Debian', lookup_arch_type('deb'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'sparcv9-redhat-linux', 'sparcv9', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'sparc64-redhat-linux', 'sparc64', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 's390-redhat-linux', 's390', lookup_arch_type('rpm'));
insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 's390-debian-linux', 's390 Debian', lookup_arch_type('deb'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 's390x-redhat-linux', 's390x', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'ppc-redhat-linux', 'ppc', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'armv7l-redhat-linux', 'armv7l', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'armv5tejl-redhat-linux', 'armv5tejl', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'armv6l-redhat-linux', 'armv6l', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'powerpc-debian-linux', 'powerpc Debian', lookup_arch_type('deb'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'ppc64-redhat-linux', 'ppc64', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'pSeries-redhat-linux', 'pSeries', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'iSeries-redhat-linux', 'iSeries', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'x86_64-redhat-linux', 'x86_64', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'ppc64iseries-redhat-linux', 'ppc64iseries', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'ppc64pseries-redhat-linux', 'ppc64pseries', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'sparc-sun4m-solaris', 'Sparc Solaris', lookup_arch_type('sysv-solaris'));
insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'sparc-sun4u-solaris', 'Sparc Solaris', lookup_arch_type('sysv-solaris'));
insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'sparc-sun4v-solaris', 'Sparc Solaris', lookup_arch_type('sysv-solaris'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'ia32e-redhat-linux', 'EM64T', lookup_arch_type('rpm'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'amd64-redhat-linux', 'AMD64', lookup_arch_type('rpm'));
insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'amd64-debian-linux', 'AMD64 Debian', lookup_arch_type('deb'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'i386-i86pc-solaris', 'i386 Solaris', lookup_arch_type('sysv-solaris'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'arm-debian-linux', 'arm Debian', lookup_arch_type('deb'));

insert into rhnServerArch (id, label, name, arch_type_id) values
(sequence_nextval('rhn_server_arch_id_seq'), 'mips-debian-linux', 'mips Debian', lookup_arch_type('deb'));

commit;

--
-- Revision 1.8  2004/05/11 18:29:40  pjones
-- bugzilla: none -- make EM64T and AMD64 registerable as such, and fix their
-- names while I'm at it.
--
-- Revision 1.7  2004/02/18 23:41:04  pjones
-- bugzilla: 116188 -- ia32e.
--
-- Revision 1.6  2004/02/06 02:21:16  misa
-- Weird solaris arches added
--
-- Revision 1.5  2004/02/05 17:33:12  pjones
-- bugzilla: 115009 -- rhnArchType is new, and has changes to go with it
--
-- Revision 1.4  2003/06/09 18:16:04  misa
-- bugzilla: 86150  Added the ppc64iseries and ppc64pseries arches, plus the channel-ppc channel arch
--
-- Revision 1.3  2003/01/29 17:11:36  misa
-- bugzilla: 83022  Adding x86_64 as a supported arch
--
-- Revision 1.2  2002/11/14 18:00:59  pjones
-- commits
--
-- Revision 1.1  2002/11/13 22:30:53  misa
-- server arch stuff: added sequence and data
--
