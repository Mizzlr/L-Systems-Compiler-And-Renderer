import sys, os
import turtle as tt

screen = tt.Screen()

class Lsystem:
	"Class to compile and draw lsytem with turtle"
	def __init__(self, save_every_frame=False,
		speed=0):
		self.name = ''
		self.variables = []
		self.constants = []
		self.axiom = ''
		self.rules = []
		self.angle = 90
		self.length = 10
		self.generation = []
		self.save_every_frame = save_every_frame
		tt.speed(speed)
	
	def __repr__(self):
		return ("<Lsystem>\n\tname: %s\n\tvariables: %s\n\t" + \
			"constants: %s\n\taxiom: %s\n\trules: %s\n\tangle:" +\
			" %s\n</Lsystem>\n") \
			% ((str(self.name), str(self.variables), 
				str(self.constants), str(self.axiom),
				str(self.rules), str(self.angle))) 

	def parse_file(self,filename):
		"method to parse a file containing Lsystem code"
		print "Parsing file %s ..." % filename
		with open(filename,'r') as infile:
			
			lines = infile.readlines()
			self.name = os.path.basename(filename).split('.')[0]
			
			for line in lines:
				split_line = line.split()
				if (split_line[0] == 'variables:'):
					self.variables = split_line[1:]
				elif (split_line[0] == 'constants:'):
					if split_line[1] != 'none':
						self.constants = split_line[1:]
				elif (split_line[0] in ['axiom:','start:']):
					self.axiom = split_line[1]
				elif (split_line[0] == 'rules:'):
					for elem in split_line[1:]:
						elem = elem[1:-1]
						a,b = elem.split('->')
						self.rules.append((a.strip(),b.strip()))
				elif (split_line[0] == 'angle:'):
					self.angle = int(split_line[1])
				elif (split_line[0] == 'length:'):
					self.length = int(split_line[1])
				elif (split_line[0].startswith('#') or \
					split_line[0] == ""):
					pass # ignore comments and empty lines
				else:
					raise Exception(
						'\n[ERROR] Cannot parse line: %s\n' % line)

			if (self.name == '' or self.variables == [] or \
				self.axiom == '' or self.rules == [] or \
				self.angle == None):
				print "[ERROR] Parsing failed. Missing some field"
				print self
				exit(1)

		print "Finished parsing"

	def compile(self, filename, number_of_generations):
		"compiles the lsystem grammar code"
		try:
			self.parse_file(filename)
		except IOError, e:
			print "[ERROR] File \"%s\" not found" % \
			 	filename
			print "\nTry any of the following from examples directory"
			print os.listdir('examples')
			print "\nExample:"
			print "python lsystem.py examples/pythagoriantree.txt 4"
			exit(1)

		print "Compiling ...",
		self.generation.append(self.axiom)
		for i in range(number_of_generations):
			self.generation.append(self.expand(self.generation[i]))
		print "Done"
		# print the generated code
		self.print_generations()

	def expand(self,string):
		"code generation with expansion technique"
		expanded_string = ''
		for character in string:
			if character in self.constants:
				expanded_string += character
			elif character in self.variables:
				for rule in self.rules:
					if rule[0] == character:
						expanded_string += rule[1]
						break
			else:
				raise Exception(
					'[ERROR] Unknown character %s in string %s\n' % \
					((character, string)))

		return expanded_string	

	def print_generations(self):
		print "Generated code:"

		for i, generation in enumerate(self.generation):
			print "[ %d ] %s\n" % ((i,generation))

	def draw(self):
		"draws the lsystem on the screen"
		stack = []
		tt.penup()
		tt.setpos(0, -200)
		tt.seth(90)
		tt.pendown()

		print "Drawing the lsystem ..."
		for i, codebit in enumerate(self.generation[-1]):

			if codebit in ['F', 'A', 'B']:
				tt.forward(self.length)
				print '[ FRWD ] ', codebit
			elif codebit == '+':
				tt.right(self.angle)
				print '[ RGHT ] ', codebit
			elif codebit == '-':
				tt.left(self.angle)
				print '[ LEFT ] ', codebit
			elif codebit == '[':
				stack.append((tt.pos(), tt.heading()))
				print '[ PUSH ] ', (tt.pos(), tt.heading())
			elif codebit == ']':
				position,heading = stack.pop()
				print '[ POP  ] ', (position, heading)
				tt.penup()
				tt.goto(position)
				tt.seth(heading)
				tt.pendown()
			else:
				print '[ NOP  ] ', codebit
			
			if self.save_every_frame:
				self.save(frame=i)

		print "Done drawing"
		print "Saving file as %s.jpg" % self.name,
		self.save()
		print "Done"

	def save(self, frame=None):
		from PIL import Image 
		import io 
		screen = tt.getscreen()
		canvas = screen.getcanvas()
		postscript = canvas.postscript().encode('utf-8')
		img = Image.open(io.BytesIO(postscript))
		if frame:
			name = self.name + "0" * (5 - len(str(frame))) + str(frame)
			img.save('pics/%s.gif' % name) 
		else:
			img.save('pics/%s.jpg' % self.name)

if __name__ == '__main__':

	# instantiate Lsystem object
	lsystem = Lsystem(save_every_frame=False, speed=0)
	# save every frame to make gif for example 
	# speed is in range of 0 to 10
	# speed (0=fastest, 1=slowest, 3=slow, 6=normal, 10=fast)
	try:
		lsystem.compile(sys.argv[1], #compile lsystem
			int(sys.argv[2])) # specify the file name
							# and generation number
		print lsystem 
		lsystem.draw() # draw lsystem with turtle
	except IndexError, e:
		print "[ERROR] Wrong usage. Use the following syntax"
		print "$ python lsystem.py filename number_of_generations\n"
		print "Example: "
		print "$ python lsystem.py examples/pythagoriantree.txt 4"
		exit(1)
