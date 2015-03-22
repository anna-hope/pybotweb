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
		if option.innerHTML is link_text
			option = $(option)
			option.remove()


$(document).ready () ->

	$('#add_link_form').submit (event) ->
		event.preventDefault()
		form = $(event.target)

		post = window.helpers.post_form form
		post.done (result) ->
			switch result['status']
				when 'success'
					link_text = $('#link_text').val()
					window.helpers.show_message "link #{link_text} added"
					add_link link_text, $('#endpoint_choice').val() + $('#variable').val()
				when 'error'
					window.helpers.show_message result['message'], error=true


	$('#remove_link_form').submit (event) ->
		event.preventDefault()
		form = $(event.target)

		post = window.helpers.post_form form
		post.done (result) =>
			switch result['status']
				when 'success'
					link_text = $('#remove_link_choice option:selected').text()
					window.helpers.show_message result['message']
					remove_link link_text
				when 'error'
					window.helpers.show_message result['message'], error=true