-- created by Oraschemadoc Wed Dec 21 14:59:56 2011
-- visit http://www.yarpen.cz/oraschemadoc/ for more info

  CREATE OR REPLACE TRIGGER "SPACEWALK"."WEB_CONTACT_MOD_TRIG" 
before insert or update on web_contact
for each row
begin
        :new.modified := sysdate;
        :new.login_uc := UPPER(:new.login);
        IF :new.password <> :old.password THEN
                :new.old_password := :old.password;
        END IF;
end;
ALTER TRIGGER "SPACEWALK"."WEB_CONTACT_MOD_TRIG" ENABLE
 
/
