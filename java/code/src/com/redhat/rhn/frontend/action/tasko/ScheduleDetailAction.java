/**
 * Copyright (c) 2011 Red Hat, Inc.
 *
 * This software is licensed to you under the GNU General Public License,
 * version 2 (GPLv2). There is NO WARRANTY for this software, express or
 * implied, including the implied warranties of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
 * along with this software; if not, see
 * http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
 *
 * Red Hat trademarks are not licensed under GPLv2. No permission is
 * granted to use or replicate Red Hat trademarks that are incorporated
 * in this software or its documentation.
 */
package com.redhat.rhn.frontend.action.tasko;

import com.redhat.rhn.common.util.RecurringEventPicker;
import com.redhat.rhn.domain.user.User;
import com.redhat.rhn.frontend.struts.RequestContext;
import com.redhat.rhn.frontend.struts.RhnAction;
import com.redhat.rhn.taskomatic.TaskomaticApi;
import com.redhat.rhn.taskomatic.TaskomaticApiException;

import org.apache.struts.action.ActionForm;
import org.apache.struts.action.ActionForward;
import org.apache.struts.action.ActionMapping;
import org.apache.struts.action.DynaActionForm;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


/**
 * ScheduleDetailAction
 * @version $Rev$
 */
public class ScheduleDetailAction extends RhnAction {

    /** {@inheritDoc} */
    public ActionForward execute(ActionMapping mapping,
                                 ActionForm formIn,
                                 HttpServletRequest request,
                                 HttpServletResponse response) {

        DynaActionForm form = (DynaActionForm)formIn;
        Map params = makeParamMap(request);
        RequestContext ctx = new RequestContext(request);
        User loggedInUser = ctx.getLoggedInUser();
        Long scheduleId = ctx.getParamAsLong(("schid"));

        if (ctx.hasParam("schid")) {
            params.put("schid", scheduleId);
            Map schedule = new HashMap();
            try {
                schedule = new TaskomaticApi().lookupScheduleById(loggedInUser, scheduleId);
            }
            catch (TaskomaticApiException e) {
                createErrorMessage(request,
                        "repos.jsp.message.taskomaticdown", null);
            }
            String scheduleName = (String) schedule.get("job_label");
            String bunchName = (String) schedule.get("bunch");
            request.setAttribute("schedulename", scheduleName);
            form.set("schedulename", scheduleName);
            request.setAttribute("bunch", bunchName);
            Boolean active = isActive(schedule);
            request.setAttribute("active", active);
            if (!active) {
                request.setAttribute("activetill", schedule.get("active_till"));
            }
        }

        prepDropdowns(ctx);
        if (!isSubmitted(form)) {
            setupForm(request, form);
            return getStrutsDelegate().forwardParams(
                    mapping.findForward("default"),
                    request.getParameterMap());
        }

        RecurringEventPicker picker = RecurringEventPicker.prepopulatePicker(
                request, "date", null);

        if (picker.isDisabled()) {
            if (scheduleId == null) {
                prepDropdowns(ctx);
                createErrorMessage(request, "message.scheduledisabled", null);

                return getStrutsDelegate().forwardParams(
                        mapping.findForward("default"), params);
            }
            return getStrutsDelegate().forwardParams(
                    mapping.findForward("disable"), params);
        }

        String scheduleName = form.getString("schedulename");
        String bunchName = form.getString("bunch");

        try {
            TaskomaticApi tapi = new TaskomaticApi();
            tapi.scheduleSatBunch(loggedInUser,
                    scheduleName,
                    bunchName,
                    picker.getCronEntry()
                    );
            if (ctx.hasParam("create_button")) {
                createSuccessMessage(request, "message.schedulecreated", scheduleName);
            }
            else {
                createSuccessMessage(request, "message.scheduleupdated", scheduleName);
            }
            Map schedule = tapi.lookupScheduleByBunchAndLabel(loggedInUser, bunchName,
                    scheduleName);
            params.put("schid", schedule.get("id"));
            return getStrutsDelegate().forwardParams(
                    mapping.findForward("success"), params);
        }
        catch (TaskomaticApiException e) {
            createErrorMessage(request,
                    "repos.jsp.message.taskomaticdown", null);
            return getStrutsDelegate().forwardParams(
                    mapping.findForward("default"), params);
        }
    }

    private Boolean isActive(Map schedule) {
        Date till = (Date) schedule.get("active_till");
        if (till == null) {
            return Boolean.TRUE;
        }
        Date now = new Date();
        return now.before(till);
    }

    private void setupForm(HttpServletRequest request, DynaActionForm form) {
        RequestContext ctx = new RequestContext(request);
        User loggedInUser = ctx.getLoggedInUser();
        Long schid = ctx.getParamAsLong("schid");

        if (schid != null) {
            try {
                TaskomaticApi tapi = new TaskomaticApi();
                Map schedule = tapi.lookupScheduleById(loggedInUser, schid);
                String scheduleName = (String) schedule.get("job_label");
                String bunchName = (String) schedule.get("bunch");
                request.setAttribute("schedulename", scheduleName);
                form.set("schedulename", scheduleName);
                request.setAttribute("bunch", bunchName);
                Map bunch = tapi.lookupBunchByName(loggedInUser, bunchName);
                request.setAttribute("bunchdescription", (String)bunch.get("description"));
                RecurringEventPicker.prepopulatePicker(request, "date",
                        (String) schedule.get(("cron_expr")));
            }
            catch (TaskomaticApiException e) {
                createErrorMessage(request,
                        "repos.jsp.message.taskomaticdown", null);
            }
        }
        else {
            RecurringEventPicker.prepopulatePicker(request, "date", null);
        }
    }

    private void prepDropdowns(RequestContext ctx) {
        User loggedInUser = ctx.getLoggedInUser();
        // populate parent base channels
        List dropDown = new ArrayList();
        try {
            List<Map> bunches = new TaskomaticApi().listSatBunchSchedules(loggedInUser);

            for (Map b : bunches) {
                addOption(dropDown, (String)b.get("name"), (String)b.get("name"));
            }
        }
        catch (TaskomaticApiException e) {
            // do not create error message, it was created before
        }
        ctx.getRequest().setAttribute("bunches", dropDown);
    }

    private void addOption(List options, String key, String value) {
        Map selection = new HashMap();
        selection.put("label", key);
        selection.put("value", value);
        options.add(selection);
    }
}
