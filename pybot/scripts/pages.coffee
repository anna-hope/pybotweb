get_current_page_asjson = () ->
	return $.get "#{location.href}?asjson=true"

show_preview = (title, content, mode) ->
	preview_div = $('<div id="page_preview"></div>')
	page_title = "<h2 class='page_title'>#{title}</h2>"
	page_article = "<article class='pybot_page'>#{content}</article>"
	close_button = """<a id='close_preview_button' data-mode=#{mode}>
						close preview</a>"""
	preview_div.append [page_title, page_article, close_button]
	preview_div.hide()

	switch mode
		when 'add' then $('#add_page').fadeOut 100
		when 'edit' then $('#edit_page').fadeOut 100

	$('#content').append preview_div
	preview_div.fadeIn 100

hide_preview = () ->
	preview_div = $('#page_preview')
	preview_div.fadeOut 100
	preview_div.remove()

show_edit_form = (title, content) ->
	edit_div = $('<div id="edit_page"></div>')
	edit_form = $('<form id="edit_page_form"></form>')
	title_input = "<input type='text' name='title' value='#{title}'>"
	content_input = """<textarea id='new_page_content' name='new_page_content'>
	#{content}</textarea>"""
	preview_button = """
	<a class="preview_button" data-mode="edit" 
		data-preview-url="#{$SITE_ROOT + '/pages/preview/'}">
		preview</a>"""
	submit_button = '<a class="submit_button">submit</a>'

	elements = [title_input, content_input, preview_button]
	edit_form.append [e, '<br>'] for e in elements
	# we want it to be on the same line
	edit_form.append submit_button

	edit_div.append edit_form

	$('#view_page').fadeOut 100
	$('#content').append edit_div

hide_edit_form = () ->
	edit_div = $('#edit_page')
	edit_div.fadeOut 100
	$('#view_page').fadeIn 100
	edit_div.remove()

update_page = () ->
	get_current_page_asjson().done (response) ->
		new_title = response['title']
		new_content = response['content_html']
		$('h2.page_title').text new_title
		$('article.pybot_page').html new_content

undelete = () ->
	delete sessionStorage['really_remove']
	warning_message = $('p.page_remove_warning')
	warning_message.fadeOut 100
	warning_message.remove()


$(document).ready () ->

	$('#page_category').change () ->
		selected_cat = $('#page_category option:selected').val()
		if selected_cat is 'new'
			$('#new_category_field').fadeIn 100
		else
			$('#new_category_field').fadeOut 100


	$('#edit_page_button').click (event) ->
		get_current_page_asjson().done (response) ->

			# we will need the slug when the user submits the edited page
			sessionStorage.slug = response['slug']
			show_edit_form response['title'], response['content_markdown']

	$('#content').on 'click', 'a.preview_button', (event) ->
		preview_button = $(event.target)
		mode = preview_button.attr 'data-mode'
		form = preview_button.parent()
		preview_url = preview_button.attr 'data-preview-url'
		result = helpers.post_form form, preview_url
		result.done (response) ->
			show_preview response['title'], response['content'], mode

	$('#content').on 'click', '#close_preview_button', () ->
		hide_preview()
		switch $(event.target).attr 'data-mode'
			when 'add' then $('#add_page').fadeIn 100
			when 'edit' then $('#edit_page').fadeIn 100

	$('#content').on 'click', 'a.submit_button', () ->
		edit_url = $('#edit_page_button').attr 'data-edit-url'
		form = $('#edit_page_form')
		result = window.helpers.post_form form, edit_url, {'slug': sessionStorage.slug}
		result.done (response) ->
			switch response['status']
				when 'success'
					update_page()
					hide_edit_form()
				when 'failure'
					window.helpers.show_message response['message'], '#content', error=true

	$('#remove_page_button').click (event) ->
		if sessionStorage.really_remove?
			[first, ..., slug, last] = location.href.split('/')
			remove_url = $(event.target).attr 'data-remove-url'
			$.post(remove_url, {'slug': slug}).done (response) ->
				switch response['status']
					when 'success'
						undelete()
						location.href = $SITE_ROOT + '/pages/'
		else
			warning_message = $("<p class='page_remove_warning'>
				you won't be able to undo this — press again if you're sure</p>")
			warning_message.hide()
			$(event.target).parent().prepend warning_message
			warning_message.fadeIn 100

			sessionStorage.really_remove = true

			# remove all that after 30 seconds if the user changes her mind
			window.setTimeout undelete, 30000


			