class Linear:
	def __init__(self, x1, x2, y1, y2):
		self.xs = sorted([x1, x2])
		self.ys = sorted([y1, y2])
	def apply(self, x):
		if x < self.xs[0] or x > self.xs[1]:
			return None
		return ((x-self.xs[0])/(self.xs[1]-self.xs[0])) * (self.ys[1]-self.ys[0]) + self.ys[0]

class Linear_table:
	def __init__(self, x_steps, y_steps):
		assert len(x_steps) == len(y_steps), 'There must be the same number for both'
		self.linears = list()
		for i in range(len(x_steps)):
			self.linears.append(Linear(*(x_steps[i] + y_steps[i])))
	def apply(self, x):
		for linear in self.linears:
			applied = linear.apply(x)
			if applied != None: return applied
		return None


US_2_5 = Linear_table([(0,12.1),(12.1,35.5),(35.5,55.5),(55.5,150.5),(150.5,250.5),(250.5,350.5),(350.5,500.5)],
		[(0, 50),(51,100),(101,150),(151,200),(201,300),(301,400),(401,500)])

US_10 = Linear_table([(0,55),(55,155),(155,255),(255,355),(355,425),(425,505),(505,605)],
		[(0, 50),(51,100),(101,150),(151,200),(201,300),(301,400),(401,500)])
