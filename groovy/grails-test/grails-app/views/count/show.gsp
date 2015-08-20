
<%@ page import="langpop.Count" %>
<!DOCTYPE html>
<html>
	<head>
		<meta name="layout" content="main">
		<g:set var="entityName" value="${message(code: 'count.label', default: 'Count')}" />
		<title><g:message code="default.show.label" args="[entityName]" /></title>
	</head>
	<body>
		<a href="#show-count" class="skip" tabindex="-1"><g:message code="default.link.skip.label" default="Skip to content&hellip;"/></a>
		<div class="nav" role="navigation">
			<ul>
				<li><a class="home" href="${createLink(uri: '/')}"><g:message code="default.home.label"/></a></li>
				<li><g:link class="list" action="index"><g:message code="default.list.label" args="[entityName]" /></g:link></li>
				<!--<li><g:link class="create" action="create"><g:message code="default.new.label" args="[entityName]" /></g:link></li>-->
			</ul>
		</div>
		<div id="show-count" class="content scaffold-show" role="main">
			<h1><g:message code="default.show.label" args="[entityName]" /></h1>
			<g:if test="${flash.message}">
			<div class="message" role="status">${flash.message}</div>
			</g:if>
			<ol class="property-list count">
			
				<g:if test="${countInstance?.count}">
				<li class="fieldcontain">
					<span id="count-label" class="property-label"><g:message code="count.count.label" default="Count" /></span>
					
						<span class="property-value" aria-labelledby="count-label"><g:fieldValue bean="${countInstance}" field="count"/></span>
					
				</li>
				</g:if>
			
				<g:if test="${countInstance?.date}">
				<li class="fieldcontain">
					<span id="date-label" class="property-label"><g:message code="count.date.label" default="Date" /></span>
					
						<span class="property-value" aria-labelledby="date-label"><g:formatDate date="${countInstance?.date}" /></span>
					
				</li>
				</g:if>
			
				<g:if test="${countInstance?.lang}">
				<li class="fieldcontain">
					<span id="lang-label" class="property-label"><g:message code="count.lang.label" default="Lang" /></span>
					
						<span class="property-value" aria-labelledby="lang-label"><g:link controller="lang" action="show" id="${countInstance?.lang?.id}">${countInstance?.lang?.encodeAsHTML()}</g:link></span>
					
				</li>
				</g:if>
			
				<g:if test="${countInstance?.site}">
				<li class="fieldcontain">
					<span id="site-label" class="property-label"><g:message code="count.site.label" default="Site" /></span>
					
						<span class="property-value" aria-labelledby="site-label"><g:link controller="site" action="show" id="${countInstance?.site?.id}">${countInstance?.site?.encodeAsHTML()}</g:link></span>
					
				</li>
				</g:if>
			
			</ol>
			<g:form url="[resource:countInstance, action:'delete']" method="DELETE">
				<fieldset class="buttons">
					<!--<g:link class="edit" action="edit" resource="${countInstance}"><g:message code="default.button.edit.label" default="Edit" /></g:link>-->
					<!--<g:actionSubmit class="delete" action="delete" value="${message(code: 'default.button.delete.label', default: 'Delete')}" onclick="return confirm('${message(code: 'default.button.delete.confirm.message', default: 'Are you sure?')}');" />-->
				</fieldset>
			</g:form>
		</div>
	</body>
</html>
