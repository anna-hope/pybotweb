$(document).ready () ->

	$('#registration_form').click (event) ->
		form = $(event.target)
		result = window.helpers.post_form form
		result.done (response) ->
			switch response['status']
				when 'success' then location.href = $SITE_ROOT
				when 'failure'
					window.helpers.show_message response['message'], parent='#content', error=true

				
			