$('document').ready () =>

	$('#run_button').click () =>
		console.log 'button pressed'

	$('#code_text').on 'click focusin', (event) =>
		code_area = $(event.target)
		if code_area.attr('data-used') is 'no'
			code_area.val ''
			code_area.attr 'data-used', 'yes'