<%@ taglib uri="http://struts.apache.org/tags-html" prefix="html" %>
<%@ taglib uri="http://rhn.redhat.com/rhn" prefix="rhn" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://struts.apache.org/tags-bean" prefix="bean" %>

<!-- enclosing head tags in layout_c.jsp -->
    <c:if test="${pageContext.request.requestURI == '/rhn/Load.do'}">
      <meta http-equiv="refresh" content="0; url=<c:out value="${param.return_url}" />" />
    </c:if>
    <meta http-equiv="content-type" content="text/html;charset=UTF-8"/>
    <title>
      <bean:message key="layout.jsp.productname"/>
      <rhn:require acl="user_authenticated()">
        <rhn:menu definition="/WEB-INF/nav/sitenav-authenticated.xml"
                  renderer="com.redhat.rhn.frontend.nav.TitleRenderer" />
      </rhn:require>
      <rhn:require acl="not user_authenticated()">
        <rhn:menu definition="/WEB-INF/nav/sitenav.xml"
                  renderer="com.redhat.rhn.frontend.nav.TitleRenderer" />
      </rhn:require>
      ${requestScope.innernavtitle}
    </title>
    <link rel="shortcut icon" href="/img/favicon.ico" />
    <link rel="stylesheet" href="/css/rhn-base.css" type="text/css" />
    <script type="text/javascript" src="/rhn/dwr/engine.js"></script>
    <script type="text/javascript" src="/rhn/dwr/util.js"></script>
    <script type="text/javascript" src="/rhn/dwr/interface/DWRItemSelector.js"></script>
    
    <script src="/javascript/prototype-1.6.0.js" type="text/javascript"> </script>
    <script src="/javascript/check_all.js" type="text/javascript"> </script>

    <!--[if IE]>
	<link rel="stylesheet" type="text/css" href="/css/rhn-iecompat.css" />
    <![endif]-->
