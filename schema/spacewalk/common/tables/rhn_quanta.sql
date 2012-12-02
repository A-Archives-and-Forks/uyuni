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


CREATE TABLE rhn_quanta
(
    quantum_id        VARCHAR2(10) NOT NULL
                          CONSTRAINT rhn_qnta0_quantum_id_pk PRIMARY KEY
                          USING INDEX TABLESPACE [[64k_tbs]],
    basic_unit_id     VARCHAR2(20),
    description       VARCHAR2(200),
    last_update_user  VARCHAR2(40),
    last_update_date  timestamp with local time zone
)
ENABLE ROW MOVEMENT
;

COMMENT ON TABLE rhn_quanta IS 'qnta0  quanta definitions';

