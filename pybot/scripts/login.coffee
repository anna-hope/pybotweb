show_error = (message) ->
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

		jqxhr = $.post $SITE_ROOT + '/login/?asjson=true', payload
		jqxhr.done (data) =>
			status = data['status']
			if status is 'success'
				window.location.href = $SITE_ROOT
			else if status is 'error'
				show_error data['message']
