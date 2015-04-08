window.helpers =
	post_form: (form, special_post_url, extra) ->
		values = form.serializeArray()
		if special_post_url?
			post_url = special_post_url
		else
			post_url = form.attr 'action'
		payload = {}
		for item in values
			payload[item['name']] = item['value']
		if extra?
			payload[key] = value for key, value of extra

		$.post "#{post_url}?asjson=true", payload

	show_message: (message, parent='body', error=false) ->
		if $('#message_div')?
			$('#message_div').remove()

		message_div = $('<div id="message_div"></div>')
		message_div.append "<p>#{message}</p>"

		if error
			message_div.css 'color', 'red'

		$(parent).append message_div

