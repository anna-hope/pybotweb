import sys
from browser import document

class ElementWriter:
	def __init__(self, dom_element_id):
		self.element = document[dom_element_id]

	def write(self, string):
		self.element <= string

sys.stdout = ElementWriter('output_area')