editing_footer = false

edit_header = () ->
	current_header = $('a.header_link')
	current_header_text = current_header.text().trim()
	new_header_text = """<input type='text'
								id='new_header_text'
			 					name='new_header_text' 
			 					value='#{current_header_text}'>"""
	current_header.hide 100
	$('header').prepend new_header_text

hide_edit_header = () ->
	$('a.header_link').show 100
	$('#new_header_text').hide 100
	$('#new_header_text').remove()

update_header = () ->
	new_header_text = $('#new_header_text').val()
	update_url = $('a.header_link').attr 'data-update-url'
	header_form = $("<form action='#{update_url}' method='POST'></form>")
	header_form.append $('#new_header_text')
	
	result = helpers.post_form header_form
	result.done (response) ->
		switch response['status']
			when 'success' then $('a.header_link').text new_header_text
			when 'failure' then helpers.show_message response['errors'], parent='header', error=true

edit_footer = () ->
	editing_footer = true
	current_footer = $('footer').text().trim()
	new_footer_input = """<input type='text'
								 id='new_footer_text'
								 name='new_footer_text'
								 value='#{current_footer}'>"""
	$('footer').html new_footer_input

update_footer = () ->
	editing_footer = false
	new_footer_input = $('#new_footer_text')
	new_footer_text = new_footer_input.val()
	update_url = $('footer').attr 'data-update-url'
	new_footer_form = $("<form action='#{update_url}' method='POST'></form>")
	new_footer_form.append new_footer_input

	result = helpers.post_form new_footer_form
	result.done (response) ->
		switch response['status']
			when 'success' then $('footer').html new_footer_text
			when 'failure' then helpers.show_message response['errors'], parent='footer', error=true 


$(document).ready () ->
	timeout = null

	$('a.header_link').mousedown () ->
		timeout = window.setTimeout edit_header, 1000

	$('a.header_link').mouseleave () ->
		window.clearTimeout timeout

	$('header').on 'keypress', '#new_header_text', (event) ->
		if event.which is 13
			# stop it from going to the result page
			event.preventDefault()
			update_header()
			hide_edit_header()

	$('footer').mousedown () ->
		if not editing_footer
			timeout = window.setTimeout edit_footer, 1000

	$('footer').mouseup () ->
		window.clearTimeout timeout

	$('footer').on 'keypress', '#new_footer_text', (event) ->
		if event.which is 13
			event.preventDefault()
			update_footer()

