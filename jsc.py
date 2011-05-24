class Variable(object):
	def __init__(self, name):
		self.name = name
	def __lshift__(self, value):
		return Assignment(self, value)
	def __str__(self):
		result = self.name
		return result
	def __repr__(self):
		return 'Variable: %s' % self
	def __getattr__(self, name):
		if name.startswith('__') or name.endswith('__'): raise AttributeError
		return Variable('.'.join([self.name, name]))
	def __call__(self, *args):
		return FuncCall(self, *args)

class FuncCall(object):
	def __init__(self, name, *args):
		self.name = str(name)
		self.args = ', '.join(str(x) for x in args)
	def __repr__(self):
		return 'FuncCall: %s(%s)' % (self.name, self.args)
	def __str__(self):
		return '%s(%s)' % (self.name, self.args)


class Expression(object):
	def __init__(self, expr):
		self.expr = expr
	def __repr__(self):
		return 'Expression: %s' % self.expr
	def __rshift__(self, args):
		if not hasattr(args, '__iter__'): args = (args,)
		return self.apply(*args)
	def apply(self, *args):
		return self.expr % args

class Assignment(object):
	template = 'var %s = %s'
	def __init__(self, name, value):
		self.name = name
		self.value = value
	def __repr__(self):
		return 'Assignment: %s, %s' % (self.name, self.value)
	def __str__(self):
		return self.template % (self.name, self.value)

class Return(object):
	template = 'return %s'
	def __init__(self, var):
		self.var = var
	def __str__(self):
		return self.template % self.var
	def __repr__(self):
		return 'Return: %s' % self

class Block(object):
	template = '{\n%s\n}'
	def __init__(self, *lines):
		self.lines = lines
	def __repr__(self): return 'Block: %d lines' % len(self.lines)
	def __str__(self):
		return self.template % ';\n'.join(str(x) for x in self.lines)

class Closure(object):
	template = '''function(%s)'''
	def __init__(self, args, *code):
		self.args = ', '.join(str(x) for x in args)
		self.code = Block(*code)
	def __str__(self):
		out = ['(',
				self.template % self.args,
				str(self.code),
				')'
			]
		return '\n'.join(out)
	def __repr__(self):
		return 'Closure: %s' % (self.template % self.args)
	def __call__(self, *args):
		return FuncCall(self, *args)

class Field(object):
	template = '''%s: %s'''
	def __init__(self, name, closure):
		self.name = name
		self.closure = closure
	def __repr__(self):
		return 'Method: %s' % self.name
	def __str__(self):
		return self.template % (self.name, self.closure)

class Object(object):
	template = '''{\n%s\n}'''
	def __init__(self, *methods):
		self.methods = methods
	def __repr__(self):
		return 'Object at %x: %d methods' % (id(self), len(self.methods))
	def __str__(self):
		methods = ',\n'.join(str(x) for x in self.methods)
		return self.template % methods

widg = Variable('widg')
jq = Variable('$')
this = Variable('this')
arguments = Variable('arguments')
print Closure((jq,),
	widg << jq.widget('"ui.captionator"', Object(
		Field('options', Object()),
		Field('_create', Closure(())),
		Field('destroy', Closure(())),
		Field('_setOption', Closure(('option', 'value'),
			jq.Widget.prototype._setOption.apply( this, arguments )
		))
	)),
	Return(widg)
)('jQuery')
