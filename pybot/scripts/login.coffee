show_error = (message) ->
	if $('#error_message')?
		console.log 'it exists!'
		$('#error_message').remove() 

	error_div = $('<div id="error_message"></div>')
	error_div.append message

	$('#content').append error_div

$(document).ready () =>

	$('#login_form').submit (event) =>
		event.preventDefault()

		email = $('#email').val()
		password = $('#password').val()
		payload =
			email: email
			password: password

		form_action = $(this).attr 'action'

		jqxhr = $.post form_action + '?asjson=true', payload
		jqxhr.done (data) =>
			status = data['status']
			if status is 'success'
				window.location.href = $HOME
			else if status is 'error'
				show_error data['message']
