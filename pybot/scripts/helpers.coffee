window.helpers =
	post_form: (form, custom_post_url, extra_values, params) ->
		values = form.serializeArray()
		if custom_post_url?
			post_url = custom_post_url
		else
			post_url = form.attr 'action'

		payload = {}
		for item in values
			payload[item['name']] = item['value']
		if extra_values?
			payload[key] = value for key, value of extra_values

		if params?
			serialized_params = $.param(params)
			$.post "#{post_url}?#{serialized_params}", payload
		else
			$.post "#{post_url}", payload

	show_message: (message, parent='body', error=false) ->
		this.hide_message()

		message_div = $('<div id="message_div"></div>')
		message_div.append "<p>#{message}</p>"

		if error
			message_div.css 'color', 'red'

		$(parent).append message_div

	hide_message: ->
		if $('#message_div')?
			$('#message_div').remove()

