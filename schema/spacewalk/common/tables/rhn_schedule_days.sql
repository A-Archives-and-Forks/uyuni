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


CREATE TABLE rhn_schedule_days
(
    recid             NUMBER(12) NOT NULL
                          CONSTRAINT rhn_schdy_recid_pk PRIMARY KEY
                          USING INDEX TABLESPACE [[2m_tbs]]
                          CONSTRAINT rhn_schdy_recid_ck
                              CHECK (recid > 0),
    schedule_id       NUMBER(12),
    ord               NUMBER(3),
    start_1           timestamp with local time zone,
    end_1             timestamp with local time zone,
    start_2           timestamp with local time zone,
    end_2             timestamp with local time zone,
    start_3           timestamp with local time zone,
    end_3             timestamp with local time zone,
    start_4           timestamp with local time zone,
    end_4             timestamp with local time zone,
    last_update_user  VARCHAR2(40),
    last_update_date  VARCHAR2(40)
)
ENABLE ROW MOVEMENT
;

COMMENT ON TABLE rhn_schedule_days IS 'schdy  individual day records for schedules';

CREATE INDEX rhn_schdy_schedule_id_idx
    ON rhn_schedule_days (schedule_id)
    TABLESPACE [[2m_tbs]];

CREATE SEQUENCE rhn_schedule_days_recid_seq;

ALTER TABLE rhn_schedule_days
    ADD CONSTRAINT rhn_schdy_sched_schedule_id_fk FOREIGN KEY (schedule_id)
    REFERENCES rhn_schedules (recid)
        ON DELETE CASCADE;

