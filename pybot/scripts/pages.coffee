show_preview = (title, content) ->
	preview_div = $('<div id="page_preview"></div>')
	page_title = "<h2 class='page_title'>#{title}</h2>"
	page_article = "<article class='pybot_page'>#{content}</article>"
	close_button = "<a id='close_preview_button'>close preview</a>"
	preview_div.append [page_title, page_article, close_button]
	preview_div.hide()

	$('#add_page').fadeOut 100
	$('#content').append preview_div
	preview_div.fadeIn 100

hide_preview = () ->
	preview_div = $('#page_preview')
	preview_div.fadeOut 100
	preview_div.remove()

show_edit = (title, content) ->
	edit_div = $('<div id="edit_div"></div>')
	title_input = "<input type='text' name='title' value='#{title}'>"
	content_input = "<textarea id='new_page_content'>#{content}</textarea>"
	preview_button = '<a class="preview_button">preview</a>'
	submit_button = '<a class="submit_button">submit</a>'

	elements = [title_input, content_input, preview_button, submit_button]
	edit_div.append elements

	$('#view_page').fadeOut 100
	$('#content').append edit_div



$(document).ready () ->

	$('#page_category').change () ->
		selected_cat = $('#page_category option:selected').val()
		if selected_cat is 'new'
			$('#new_category_field').fadeIn 100
		else
			$('#new_category_field').fadeOut 100


	$('#edit_page_button').click (event) ->
		edit_url = $(event.target).attr 'data-edit_url'
		$.get "#{location.href}?asjson=true", (response) ->
			show_edit response['title'], response['content_markdown']

	$('#content').on 'click', 'a.preview_button', (event) ->
		form = $('#add_page_form')
		preview_url = $(event.target).attr 'data-preview_url'
		result = helpers.post_form form, preview_url
		result.done (response) ->
			show_preview response['title'], response['content']

	$('#content').on 'click', '#close_preview_button', () ->
		hide_preview()
		$('#add_page').fadeIn 100