<%@ taglib uri="http://struts.apache.org/tags-html" prefix="html" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://rhn.redhat.com/rhn" prefix="rhn" %>
<%@ taglib uri="http://struts.apache.org/tags-bean" prefix="bean" %>
<%@ taglib uri="http://rhn.redhat.com/tags/list" prefix="rl" %>

<html:xhtml/>
<html>
<body>

<rhn:toolbar base="h1" img="/img/rhn-icon-your_rhn.gif"
             imgAlt="channels.overview.toolbar.imgAlt"
             creationUrl="/rhn/admin/ScheduleDetail.do"
             creationType="schedule"
             creationAcl="user_role(satellite_admin)"
	         helpUrl="">
    <bean:message key="task.status.title"/>
</rhn:toolbar>

<rl:listset name="scheduleList">

    <rl:list
        emptykey="schedule.jsp.noschedules">

                <rl:decorator name="PageSizeDecorator"/>

                <rl:column sortable="true"
                           bound="false"
                           styleclass="first-column last-column"
                           headerkey="schedule.edit.jsp.name"
                           sortattr="job_label"
                           defaultsort="asc"  >
                        <a href="/rhn/admin/ScheduleDetail.do?schid=${current.id}">${current.job_label}</a>
                </rl:column>

                <rl:column bound="false"
                           headerkey="schedule.edit.jsp.frequency" >
                        <c:out value="${current.cron_expr}" />
                </rl:column>

                <rl:column sortable="true"
                           bound="false"
                           headerkey="schedule.edit.jsp.activefrom"
                           sortattr="active_from" >
                        <c:out value="${current.active_from}" />
                </rl:column>

                <rl:column bound="false"
                           headerkey="schedule.edit.jsp.bunch" >
                         <a href="/rhn/admin/BunchDetail.do?label=${current.bunch}">${current.bunch}</a>
                </rl:column>

</rl:list>
</rl:listset>

</body>
</html>
