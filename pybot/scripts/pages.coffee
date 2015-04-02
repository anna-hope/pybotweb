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
	$('#add_page').fadeIn 100
	preview_div.remove()


$(document).ready () ->

	$('#page_category').change () ->
		selected_cat = $('#page_category option:selected').val()
		if selected_cat is 'new'
			$('#new_category_field').fadeIn 100
		else
			$('#new_category_field').fadeOut 100

	$('a.preview_button').click (event) ->
		form = $('#add_page_form')
		preview_url = $(event.target).attr 'data-preview_url'
		result = helpers.post_form form, preview_url
		result.done (response) ->
			show_preview response['title'], response['content']

	$('#content').on 'click', '#close_preview_button', () ->
		hide_preview()