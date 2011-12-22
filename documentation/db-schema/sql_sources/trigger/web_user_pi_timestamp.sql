-- created by Oraschemadoc Wed Dec 21 14:59:57 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE TRIGGER "SPACEWALK"."WEB_USER_PI_TIMESTAMP" 
BEFORE INSERT OR UPDATE ON web_user_personal_info
FOR EACH ROW
BEGIN
  :new.modified := sysdate;
END;
ALTER TRIGGER "SPACEWALK"."WEB_USER_PI_TIMESTAMP" ENABLE
 
/
