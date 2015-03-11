run_brython = () ->
	if $DEBUG
		brython(1)
	else
		brython()

$('document').ready () =>
	run_brython()

	mcm = CodeMirror.fromTextArea(document.getElementById 'code_text',
									{mode: 'Python'})

	$('#run_button').click () =>
		mcm.save()
		code_area = $('#code_text')
		user_code = code_area.val()

		# hack to stop code from piling up
		# (replace with something better)
		$('#brython_code').remove()
		$('#output_area').empty()

		code_section = $('<script type="text/python" id="brython_code"></script>')
		code_section.text user_code

		$('#content').append code_section
		run_brython()

	$('div.CodeMirror').on 'click focusin', (event) =>
		code_area = $('#code_area')
		if code_area.attr('data-used') is 'no'
			code_area.attr 'data-used', 'yes'
			mcm.setValue ''

	# $('#code_area').on 'click focusin', (event) =>
	# 	code_area = $(event.target)
	# 	if code_area.attr('data-used') is 'no'
	# 		console.log 'focused'
	# 		mcm.setValue ''
	# 		console.log mcm.getValue()
	# 		code_area.attr 'data-used', 'yes'