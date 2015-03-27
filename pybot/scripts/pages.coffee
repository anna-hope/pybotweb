$(document).ready () ->

	$('#page_category').change () ->
		selected_cat = $('#page_category option:selected').val()
		if selected_cat is 'new'
			$('#new_category_field').fadeIn 100
		else
			$('#new_category_field').fadeOut 100

	$('a.preview_button').click () ->
		console.log 'there will be a preview'