window.admin_helpers = 
	add_link: (links_list, link_text, url) ->
		new_link = "<li><a href='#{url}'>#{link_text}</a></li> "
		$(links_list).append new_link
		$('#remove_link_choice').append "<option value='#{link_text}'>#{link_text}</option>"

	remove_link: (links_list, link_text) ->
		links = $(links_list).children()
		add_link_choices = $('#remove_link_choice').children()

		for link in links
			link = $(link)
			if link.text() is link_text
				link.remove()

		for option in add_link_choices
			if option.innerHTML is link_text
				option = $(option)
				option.remove()

	populate_subpage_select: (select_element) ->
		variable_field = $('<select id="variable" name="variable"></select>') 
		$(select_element).replaceWith variable_field
		$.get('/pages/get_all').done (response) ->
			options = "<option value='#{slug}'>#{page_title}</option>" for page_title, slug of response
			variable_field.append options
