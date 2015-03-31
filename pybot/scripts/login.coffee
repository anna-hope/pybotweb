$(document).ready () =>

	$('#login_form').submit (event) =>
		event.preventDefault()

		post = window.helpers.post_form $(event.target)
		post.done (result) ->
			switch result['status']
				when 'success'
					next = location.search.split('next=')[1]
					if next?
						location.href = decodeURIComponent next
					else
						location.href = $HOME
				when 'error' then window.helpers.show_message result['message'], parent='#content', error=true