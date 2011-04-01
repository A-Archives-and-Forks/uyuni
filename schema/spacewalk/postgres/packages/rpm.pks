-- oracle equivalent source sha1 1f8b5508a1d7ce29135f848b78b6564d005747b8
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

create schema rpm;

--update pg_setting
update pg_settings set setting = 'rpm,' || setting where name = 'search_path';

CREATE OR REPLACE FUNCTION isdigit(ch CHAR)
RETURNS BOOLEAN
AS $$
BEGIN
  RAISE EXCEPTION 'Stub called, must be replaced by .pkb';
END ;
$$ language 'plpgsql';

CREATE OR REPLACE FUNCTION isalpha(ch CHAR)
RETURNS BOOLEAN
AS $$
BEGIN
  RAISE EXCEPTION 'Stub called, must be replaced by .pkb';
END;
$$ language 'plpgsql';

CREATE OR REPLACE FUNCTION isalphanum(ch CHAR)
RETURNS BOOLEAN
AS $$ 
BEGIN
  RAISE EXCEPTION 'Stub called, must be replaced by .pkb';
END;
$$ language 'plpgsql';

CREATE OR REPLACE FUNCTION rpmstrcmp (string1 IN VARCHAR, string2 IN VARCHAR)
RETURNS INTEGER
AS $$
BEGIN
  RAISE EXCEPTION 'Stub called, must be replaced by .pkb';
END ;
$$ language 'plpgsql';

CREATE OR REPLACE FUNCTION vercmp(
        e1 VARCHAR, v1 VARCHAR, r1 VARCHAR, 
        e2 VARCHAR, v2 VARCHAR, r2 VARCHAR)
RETURNS INTEGER
AS $$
BEGIN
  RAISE EXCEPTION 'Stub called, must be replaced by .pkb';
END;
$$ language 'plpgsql';

-- restore the original setting
update pg_settings set setting = overlay( setting placing '' from 1 for (length('rpm')+1) ) where name = 'search_path';
