from . import common

class Qct:
	def __init__(self):
		self.username = common.set_username()
		# If all QCT will have a form number, call it here, not in each subclass...
		self.formnumber = common.set_formnumber()
		self.doc_char = "A" # starting letter for supplemental documents
	
