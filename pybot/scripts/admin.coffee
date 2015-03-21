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
	$('#link').append "<option value='#{link_text}'>#{link_text}</option>"

remove_link = (link_text) ->
	links = $('.links_list').children()

	for link in links
		link = $(link)
		if link.text() is link_text
			link.remove()


$(document).ready () ->

	$('#add_link_form').submit (event) ->
		event.preventDefault()
		form_action_url = $(event.target).attr 'action'

		link_text = $('#link_text').val()
		url = $('#url').val()
		variable = $('#variable').val()
		payload =
			link_text: link_text
			url: url
			variable: variable

		jqxhr = $.post form_action_url + '?asjson=true', payload
		jqxhr.done (data) =>
			if data['status'] is 'success'
				show_message data['message']
				add_link link_text, url + variable
			else
				show_message data['message'], error=true

	$('#remove_link_form').submit (event) ->
		event.preventDefault()
		form_action_url = $(event.target).attr 'action'

		link_text = $('#link').val()
		payload = {link: link_text}

		jqxhr = $.post form_action_url + '?asjson=true', payload
		jqxhr.done (data) =>
			if data['status'] is 'success'
				show_message data['message']
				remove_link link_text
			else
				show_message data['message'], error=true