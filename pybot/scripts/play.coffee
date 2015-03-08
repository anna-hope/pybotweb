$('document').ready () =>

	$('#run_button').click () =>
		code_area = $('#code_text')
		user_code = code_area.val()

		# hack to stop code from piling up
		# (replace with something better)
		$('#brython_code').remove()

		code_section = $('<script type="text/python" id="brython_code"></script>')
		code_section.text user_code

		$('#content').append code_section
		if $DEBUG
			brython(1)
		else
			brython()

	$('#code_text').on 'click focusin', (event) =>
		code_area = $(event.target)
		if code_area.attr('data-used') is 'no'
			code_area.val ''
			code_area.attr 'data-used', 'yes'