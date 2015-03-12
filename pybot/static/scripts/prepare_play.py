import sys
from browser import document, html

class ElementWriter:
	def __init__(self, dom_element_id):
		self.element = document[dom_element_id]

	def write(self, string):
		output_element = html.P(string)
		self.element <= output_element

class ErrorWriter(ElementWriter):
	def write(self, string):
		error_div = html.DIV(string, id='error_output',
							 style={'color': 'red'})
		self.element <= error_div

sys.stdout = ElementWriter('output_area')
sys.stderr = ErrorWriter('output_area')