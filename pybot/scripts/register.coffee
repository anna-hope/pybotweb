$(document).ready () ->

	$('#registration_form').submit (event) ->
		event.preventDefault()
		form = $(event.target)
		result = window.helpers.post_form form
		result.done (response) ->
			switch response['status']
				when 'success' then location.href = $HOME
				when 'failure'
					helpers.show_message response['errors'], parent='#content', error=true