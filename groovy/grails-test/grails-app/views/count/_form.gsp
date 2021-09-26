<%@ page import="langpop.Count" %>



<div class="fieldcontain ${hasErrors(bean: countInstance, field: 'count', 'error')} required">
	<label for="count">
		<g:message code="count.count.label" default="Count" />
		<span class="required-indicator">*</span>
	</label>
	<g:field name="count" type="number" value="${countInstance.count}" required=""/>

</div>

<div class="fieldcontain ${hasErrors(bean: countInstance, field: 'date', 'error')} required">
	<label for="date">
		<g:message code="count.date.label" default="Date" />
		<span class="required-indicator">*</span>
	</label>
	<g:datePicker name="date" precision="day"  value="${countInstance?.date}"  />

</div>

<div class="fieldcontain ${hasErrors(bean: countInstance, field: 'lang', 'error')} required">
	<label for="lang">
		<g:message code="count.lang.label" default="Lang" />
		<span class="required-indicator">*</span>
	</label>
	<g:select id="lang" name="lang.id" from="${langpop.Lang.list()}" optionKey="id" required="" value="${countInstance?.lang?.id}" class="many-to-one"/>

</div>

<div class="fieldcontain ${hasErrors(bean: countInstance, field: 'site', 'error')} required">
	<label for="site">
		<g:message code="count.site.label" default="Site" />
		<span class="required-indicator">*</span>
	</label>
	<g:select id="site" name="site.id" from="${langpop.Site.list()}" optionKey="id" required="" value="${countInstance?.site?.id}" class="many-to-one"/>

</div>

