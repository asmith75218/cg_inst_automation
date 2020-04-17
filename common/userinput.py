class Userinput:
	def __init__(self, user_input_string):
		self.user_response = user_input_string
		
	def valid_range(self, nrange):
		try:
			return int(self.user_response) in nrange
		except ValueError:
			return False
			
	def valid_type(self, ntype):
		return isinstance(self.user_response, ntype)
		
	def valid_len(self, nlen, *args):
		if 'max' in args:
			return len(self.user_response) <= nlen
		elif 'min' in args:
			return len(self.user_response) >= nlen
		else:
			return len(self.user_response) == nlen
			
	def valid_name(self):
		## TODO: name validation logic here
		
		# meanwhile, everything passes
		return True