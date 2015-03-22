show_message = (message, error=false, parent='body') ->
	if $('#message_div')?
		$('#message_div').remove()

	message_div = $('<div id="message_div"></div>')
	message_div.append "<p>#{message}</p>"

	if error
		message_div.css 'color', 'red'

	$(parent).append message_div

add_link = (link_text, url) ->
	new_link = "<li><a href='#{url}'>#{link_text}</a></li>"
	$('.links_list').append new_link
	$('#remove_link_choice').append "<option value='#{link_text}'>#{link_text}</option>"

remove_link = (link_text) ->
	links = $('.links_list').children()
	add_link_choices = $('#remove_link_choice').children()

	for link in links
		link = $(link)
		if link.text() is link_text
			link.remove()

	for option in add_link_choices
		console.log option
		if option.innerHTML is link_text
			option = $(option)
			option.remove()


$(document).ready () ->

	$('#add_link_form').submit (event) ->
		event.preventDefault()
		form_action_url = $(event.target).attr 'action'

		link_text = $('#link_text').val()
		endpoint = $('#endpoint_choice').val()
		variable = $('#variable').val()
		payload =
			link_text: link_text
			endpoint_choice: endpoint
			variable: variable

		jqxhr = $.post form_action_url + '?asjson=true', payload
		jqxhr.done (data) =>
			if data['status'] is 'success'
				show_message data['message']
				add_link link_text, $('#endpoint_choice').text() + variable
			else
				show_message data['message'], error=true

	$('#remove_link_form').submit (event) ->
		event.preventDefault()
		form_action_url = $(event.target).attr 'action'

		link_text = $('#remove_link_choice').val()
		payload = {remove_link_choice: link_text}

		jqxhr = $.post form_action_url + '?asjson=true', payload
		jqxhr.done (data) =>
			if data['status'] is 'success'
				show_message data['message']
				remove_link link_text
			else
				show_message data['message'], error=true