$(document).ready () ->
	$('div.admin_panel').hide()
	admin_helpers.populate_subpage_select('#variable')

	$('a.admin_panel_link').click (event) ->
		form_name = $(event.target).attr 'data-form'
		$('#' + form_name).toggle 100

	$('#add_link_form').submit (event) ->
		event.preventDefault()
		form = $(event.target)
		post = window.helpers.post_form form, null, null, params={'asjson':true}
		post.done (result) ->
			switch result['status']
				when 'success'
					link_text = $('#link_text').val()
					window.helpers.show_message "link #{link_text} added"
					admin_helpers.add_link(
						'ul.links_list', link_text, 
						$('#endpoint_choice option:selected').text() + $('#variable').val())
				when 'error'
					window.helpers.show_message result['message'], error=true

	$('#endpoint_choice').change (event) ->
		if $('#endpoint_choice option:selected').val() is 'render_page'
			$('#variable').show()
		else
			$('#variable').hide()


	$('#remove_link_form').submit (event) ->
		event.preventDefault()
		form = $(event.target)

		post = window.helpers.post_form form
		post.done (result) ->
			switch result['status']
				when 'success'
					link_text = $('#remove_link_choice option:selected').text()
					window.helpers.show_message result['message']
					admin_helpers.remove_link 'ul.links_list', link_text
				when 'error'
					window.helpers.show_message result['message'], error=true

	$('#change_header_form').submit (event) ->
		event.preventDefault()
		form = $(event.target)

		post = window.helpers.post_form form
		post.done (result) ->
			switch result['status']
				when 'success' then window.helpers.show_message result['message']
				when 'error' then window.helpers.show_message result['message'], error=true

	$('#change_footer_form').submit (event) ->
		event.preventDefault()
		form = $(event.target)

		post = window.helpers.post_form form
		post.done (result) ->
			switch result['status']
				when 'success'
					$('footer').empty()
					$('footer').append "<p>#{$('#new_footer_text').val()}</p>"
				when 'error'
					window.helpers.show_message result['message'], error=true

	$('#generate_token_button').click (event) ->
		button  = $(event.target)
		generate_url = button.attr 'data-url'
		result = $.get generate_url
		result.done (response) ->
			[first, middle, last] = window.location.href.split('/') 
			$('#generate_tokens').append """<p>
			<a href='#{middle}#{response['message']}'>#{response['message']}</a>
			</p>"""