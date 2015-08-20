
<%@ page import="langpop.Count" %>
<!DOCTYPE html>
<html>
    <head>
        <meta name="layout" content="main">
        <g:set var="entityName" value="${message(code: 'count.label', default: 'Count')}" />
        <title><g:message code="default.list.label" args="[entityName]" /></title>
    </head>
    <body>
        <a href="#list-count" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
        <div class="nav" role="navigation">
            <ul>
                <li><a class="home" href="${createLink(uri: '/')}"><g:message code="default.home.label"/></a></li>
            </ul>
        </div>
        <div id="list-count" class="content scaffold-list" role="main">
            <h1><g:message code="default.list.label" args="[entityName]" /></h1>
            <g:if test="${flash.message}">
                <div class="message" role="status">${flash.message}</div>
            </g:if>
            <table>
            <thead>
                    <tr>
                    
                        <g:sortableColumn property="count" title="${message(code: 'count.count.label', default: 'Count')}" />
                    
                        <g:sortableColumn property="date" title="${message(code: 'count.date.label', default: 'Date')}" />
                    
                        <th><g:message code="count.lang.label" default="Lang" /></th>
                    
                        <th><g:message code="count.site.label" default="Site" /></th>
                    
                    </tr>
                </thead>
                <tbody>
                <g:each in="${countInstanceList}" status="i" var="countInstance">
                    <tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
                    
                        <td><g:link action="show" id="${countInstance.id}">${fieldValue(bean: countInstance, field: "count")}</g:link></td>
                    
                        <td><g:formatDate date="${countInstance.date}" /></td>
                    
                        <td>${fieldValue(bean: countInstance, field: "lang.name")}</td>
                    
                        <td>${fieldValue(bean: countInstance, field: "site.name")}</td>
                    
                    </tr>
                </g:each>
                </tbody>
            </table>
        </div>
    </body>
</html>
