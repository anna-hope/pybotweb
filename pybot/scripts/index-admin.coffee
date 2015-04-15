timeout = null
editing = false

edit_index_message = () ->
	editing = true

	index_message_div = $('#index_message')
	current_message_text = index_message_div.text().trim()

	textarea_name = 'new_message_text'
	new_message_textarea = """<textarea id=#{textarea_name} name=#{textarea_name}>
								#{current_message_text}
								</textarea>"""
	submit_button = '''<br><a class="submit_button">
						update the message</a>'''
	edit_index_message_div = $('<div id="edit_index_message_div"></div>')
	edit_index_message_div.append [new_message_textarea, submit_button]

	index_message_div.empty()
	index_message_div.append edit_index_message_div

update_index_message = () ->
	new_message_textarea = $('#new_message_text')
	new_message_form = $('<form action="/update_index_message/" method="POST"></form>')
	new_message_form.append new_message_textarea
	result = helpers.post_form new_message_form
	result.done (response) ->
		switch response['status']
			when 'success'
				$('#index_message').html response['new_message']
				new_message_form.remove()
				new_message_textarea.remove()
				editing = false
			when 'failure'
				helpers.show_message response['message'], parent='#index_message', error=true
		
$(document).ready () ->

	$('#index_message').mousedown () ->
		if not editing
			timeout = window.setTimeout edit_index_message, 1500

	$('#index_message').mouseup () ->
		window.clearTimeout timeout

	$('#index_message').on 'click', 'a.submit_button', (event) ->
		update_index_message()