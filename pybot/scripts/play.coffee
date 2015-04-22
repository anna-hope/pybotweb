

run_brython = ->
	if $DEBUG
		brython(1)
	else
		brython()

run_play = (mcm) ->
	mcm.save()
	code_area = $('#code_text')
	user_code = code_area.val()

	$('#brython_code').remove()
	$('#output_area').empty()

	code_section = $('<script type="text/python" id="brython_code"></script>')
	code_section.text user_code

	$('#content').append code_section
	run_brython()

$('document').ready () ->	
	run_brython()
	mcm = CodeMirror.fromTextArea(document.getElementById 'code_text',
									{mode: 'Python'})

	$('#run_button').click () ->
		run_play(mcm)

	$('div.CodeMirror').on 'click focusin', () ->
		console.log 'hi'
		code_area = $('#code_area')
		if code_area.attr('data-used') is 'no'
			code_area.attr 'data-used', 'yes'
			mcm.setValue ''