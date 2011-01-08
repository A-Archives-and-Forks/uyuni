--
-- Copyright (c) 2008--2010 Red Hat, Inc.
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

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '5326810137017186', lookup_package_key_type('gpg'), lookup_package_provider('Red Hat Inc.'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '219180cddb42a60e', lookup_package_key_type('gpg'), lookup_package_provider('Red Hat Inc.'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), 'b44269d04f2a6fd2', lookup_package_key_type('gpg'), lookup_package_provider('Fedora'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), 'a8a447dce8562897', lookup_package_key_type('gpg'), lookup_package_provider('CentOS'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '2802e89216ff0e46', lookup_package_key_type('gpg'), lookup_package_provider('CentOS'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), 'a53d0bab443e1821', lookup_package_key_type('gpg'), lookup_package_provider('CentOS'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '7049e44d025e513b', lookup_package_key_type('gpg'), lookup_package_provider('CentOS'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '25dbef78a7048f8d', lookup_package_key_type('gpg'), lookup_package_provider('Scientific Linux'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '66ced3de1e5e0159', lookup_package_key_type('gpg'), lookup_package_provider('Oracle Inc.'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '2e2bcdbcb38a8516', lookup_package_key_type('gpg'), lookup_package_provider('Oracle Inc.'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), 'a84edae89c800aca', lookup_package_key_type('gpg'), lookup_package_provider('SUSE LINUX Products GmbH'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '1dc5c758d22e77f2', lookup_package_key_type('gpg'), lookup_package_provider('Fedora'));

-- Fedora 12
insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '9d1cc34857bbccba', lookup_package_key_type('gpg'), lookup_package_provider('Fedora'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '95423d4e430a1c35', lookup_package_key_type('gpg'), lookup_package_provider('Spacewalk'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), 'e3a5c360307e3d54', lookup_package_key_type('gpg'), lookup_package_provider('SUSE LINUX Products GmbH'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '6c74ce73b37b98a9', lookup_package_key_type('gpg'), lookup_package_provider('SUSE LINUX Products GmbH'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '2afe16421d061a62', lookup_package_key_type('gpg'), lookup_package_provider('Novell Inc.'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '14c28bc97e2e3b05', lookup_package_key_type('gpg'), lookup_package_provider('Novell Inc.'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '478a32e8a1912208', lookup_package_key_type('gpg'), lookup_package_provider('Novell Inc.'));

insert into rhnPackageKey (id, key_id, key_type_id, provider_id) values
(sequence_nextval('rhn_pkey_id_seq'), '73d25d630dfb3188', lookup_package_key_type('gpg'), lookup_package_provider('Novell Inc.'));

commit;

--
-- Revision 1.1  2008/07/02 23:42:28  jsherrill
-- Sequence; data to populate stuff
--

