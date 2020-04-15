class Userinput:
	def __init__(self, response):
		self.user_response = response
		
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