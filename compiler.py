# Nikolaos Zamparas
# AM: 2969
# Username: cse52969
# Compiler version 1.0

'''
### Changelog ###
Version 1.0 - FINAL:
- [FINAL CODE]: -Now works for functions.
				-Fixed some bugs in loadvr and storerv
				-Fixed some issues in the generation of main's assembly
				 code

This version is considered as the final version of the Compiler.
=======================================================================
Version 0.9.9 - BETA 2:
[FINAL_CODE]: -Tested for simple programs without functions
			  -Now syscall-10 is called after reading the halt-quad
#TODO: Fix Final code for functions
========================================================================
Version 0.9 - BETA 1:
- [FINAL_CODE]: Final code implementation is complete. Compiles in MARS
				without issues.
- [C CODE]	  :	Implemented better Warning messages

- This version is considered the first BETA version of the compiler 

#TODO: Make the mips code not just compile, but run too :)
#TODO: Delete scopes after the generation of the final code.
#TODO (Fixed!): Check error handler's line printing 
==========================================================================
Version 0.8:
- [FINAL_CODE]: First implementation of full final code generation is ready
==========================================================================
Version 0.7:
- [FINAL_CODE]: Implemented non-fuction related code generation
- [WARNING_HANDLER]: Implemented.
===========================================================================
Version 0.6:
- [FINAL_CODE]: gnvlcode, loadvr, storerv are ready
===========================================================================
Version 0.5.1:
- Tweaked function parameter generation to include the creation of a 
	new argument instead of just passing a parameter_type entity as a 
	function argument.
============================================================================
Version 0.5:
- Version 0.5 is considered ready for Phase 3 (Symbol Table).
- [SYN-QUADS]:	Added quads code to support assignment of function results in variables
			 	[x := function()]
- Completed Symbol Table functions and generation!
============================================================================
Version 0.4:
- Basic Symbol Table functionality is now OK
- [ERROR_HANDLER]: Added error line printing 
- [SYN] Fixed major bug in syn made by a misunderstanding of Minimal++ Grammar. 

#TODO (Fixed!) [URGENT]: Support nested functions. Problem caused when reading
				the '{' symbol after function's definition in funcbody. 
				Statements need it to work properly, but declarations and 
				subprograms need the next token.
==============================================================================
Version 0.3.6:
- Fixed (most) SYN bugs. That was tough..:P
- Added changelog printing

#TODO: Fix "minus" bug in intermediate code. Check expression, factor
#TODO (?): Update intermediate and c code generation functions to support function calls.
#TODO (?): Check which variables are declared in C code (Symbol table will help on that)
#TODO (Fixed!): Report an error if a comment is inside a comment
				LEX now skips comments inside comments
==============================================================================
Version 0.3.5:
- Completed Symbol Table Code
- Checked Symbol Table code

#TODO (URGENT) (Fixed in 0.3.6): Fix SYN bugs (begin with factor and itdail)
#TODO: Report an error if a comment is inside a comment
#TODO (OK): Check function and variable (int) types. What does it refers to?
==============================================================================
Version 0.3.1:
- Added Symbol Table types
- Added (some) Symbol Table Actions

#TODO (Fixed!): Better check function actions
==============================================================================
Version 0.3:
- SYN: Added Intermediate Code Generation Ability
- Some minor changes to help() function for better eyecandy!
- Added C code generation
- Fixed minor Label writing issue to C code

# TODO: Implement call intermediate & C code
# TODO (Fixed!): Now can pass negative values correctly to intermediate code and C code 
# TODO (Fixed!): Implement quads for forcase_stat
# TODO (Fixed!): Catch an error in syn (test again with and without ';' inside ifs)
# TODO (Fixed!): .int -> .c code convertion...
==============================================================================
Version 0.2:
- SYN: 				Is now fixed, works with my tests
- LEX: 				Added skip comment ability
- ERROR_HANDLER: 	Added color and bold-letters printing ability

# TODO: print error line/column, start working on next phase's code
===============================================================================
First Version:
- LEX: 				Implemented, no comments skip
- SYN:				Implemented first version of SYN

# TODO: skip_comment in LEX, fix some stuff in SYN, print error line/column too
'''

import sys 								
import os
import inspect	# for debug reasons

version = "1.0-FINAL"
changelog = "[FINAL CODE]:\n\
-Now works for functions.\n\
-Fixed some bugs in loadvr and storerv\n\
-Fixed some issues in the generation of main's assembly code\n\n\
This version is considered as the final version of the Compiler."


NUM_OP = {"+":"add-oper_tk", "-":"add-oper_tk", "*":"mul-oper_tk", "/":"mul-oper_tk"}
ASSIGN_OP = {":=":"assign-op_tk"}
SEPERATOR = {";":"semicolon_tk", ",":"comma_tk", ":":"colon_tk"}
GROUP_OP = {"(":"open-paren_tk", ")":"close-paren_tk", "[":"open-bracket_tk", "]":"close-bracket_tk", "{":"open-hook_tk", "}":"close-hook_tk"}
COMMENT = {"//":"line-comment_tk", "/*":"open-comment_tk", "*/":"close-comment_tk"}
COMP_OP = {"<":"less-than_tk",">":"greater-than_tk","=":"equal_tk","<=":"less-or-equal_tk",">=":"greater-or-equal_tk","<>":"not-equal_tk"}

KEYWORDS = {"program":"keyword-program_tk","declare":"keyword-declare_tk","if":"keyword-if_tk", "then":"keyword-then_tk", 
"else":"keyword-else_tk", "while":"keyword-while_tk", "doublewhile":"keyword-doublewhile_tk", "loop":"keyword-loop_tk", 
"exit":"keyword-exit_tk","forcase":"keyword-forcase_tk", "incase":"keyword-incase_tk", "when":"keyword-when_tk", "default":"keyword-default_tk", 
"function":"keyword-function_tk", "return":"keyword-return_tk", "in":"keyword-in_tk", 
"inout":"keyword-inout_tk", "and":"keyword-and_tk", "or":"keyword-or_tk", "not":"keyword-not_tk",
"input":"keyword-input_tk", "print":"keyword-print_tk", "procedure":"keyword-procedure_tk", "call":"keyword-call_tk"}


next_letter = ''
current_letter = ''
line = 1

class color: # some nice colors for printing text!
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'

def print_version():
	print("Compiler Version: "+color.CYAN+str(version)+color.END+'\n')

def print_progress():																		
	print_version()
	print("Progress in this version includes:")
	print(changelog)

def help():
	print_version()
	print("Usage:")
	print("python3 compiler.py <sourcefile>              : Compile and save to <out.asm>")
	print("python3 compiler.py <sourcefile> <outfile>    : Compile and save to <outfile.asm>")
	print("python3 compiler.py -h (or) --help            : Print this help message")
	print("\nVersion Info:\npython3 compiler.py --changelog               : Print this version's changelog")

def error_handler(c):
	global token_value, line
	if token_value == None:
		print(color.RED + "[ERROR] " + str(c) + color.END)
		sys.exit()
	print(color.RED + "[ERROR] ", c + " in line " + str(line) + color.END)
	print(color.RED + "Last read character: " + token_value + color.END)
	print(color.RED +  "\n[DEBUG-INFO] Error raised by function: "  + inspect.stack()[1][3] + color.END)
	sys.exit(1)

def warning_handler(w, kill_switch = False):
	if kill_switch:
		print(color.YELLOW+"[WARNING] "+str(w)+color.END)
		error_handler(str(w))
	else:
		print(color.YELLOW+"[WARNING] "+str(w)+color.END)

def check_arguments():
	if len(sys.argv) > 3:
		print("Less arguments expected, use -h for help.")
		sys.exit() 	
	elif len(sys.argv) == 1:
		help()
		sys.exit()
	if (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
		help()
		sys.exit()
	if (sys.argv[1] == "--changelog"):
		print_progress()
		sys.exit()

def skip_blank():
	global source_file, line
	current_letter = source_file.read(1)
	if current_letter == '\n':
		line += 1
	if current_letter.isspace():
		skip_blank()
	else:
		try:
			source_file.seek(source_file.tell()-1)
		except ValueError:
			error_handler("Empty source file")
			sys.exit()

def peek_next_letter():
	global current_letter, next_letter, source_file
	next_letter = source_file.read(1)
	source_file.seek(source_file.tell()-1)
	return next_letter

def joined(c):
	return ''.join(c)

# LEX: ------------------------------------------------------------------------

def lex(): 
	# LEX returns: <token, token description>
	global source_file, current_letter, next_letter
	global line
	current_tk = []
	skip_blank()
	while (1):
		
		current_letter = source_file.read(1)
		if current_letter == '\n':
			line += 1
		if len(current_letter) < 1:
			return "EOF", "EOF_tk"
		if current_letter.isspace():
			continue
		next_letter = peek_next_letter()

		# Check (and remove) COMMENT (2-char operator always):
		if (current_letter == "/") or (current_letter == "*"):
			current_tk.append(current_letter)
			current_tk.append(next_letter)
			if (joined(current_tk) in COMMENT): # found a comment operator, now process the comment
				source_file.seek(source_file.tell()+1)

				# Found a comment! (Don't return it, deal with it):
				if joined(current_tk) == "/*":
					while(1):
						current_letter = source_file.read(1)
						if current_letter == '\n':
							line += 1
						next_letter = peek_next_letter()
						if (current_letter == "*" and next_letter == "/"):
							try:
								current_tk.remove("/")
								current_tk.remove("*")
							except:
								pass
							current_tk.append(current_letter)
							current_tk.append(next_letter)
							if joined(current_tk) in COMMENT:
								try:
									current_tk.remove("/")
									current_tk.remove("*")
									# prepare current_letter and next_letter to be used 
									# from lex() like nothing happened
									current_letter = source_file.read(1)
									if current_letter == '\n':
										line += 1
									next_letter = peek_next_letter()
									current_letter = source_file.read(1)
									if current_letter == '\n':
										line += 1
									next_letter = peek_next_letter()
								except:
									pass
								break
				else: # it's a line comment
					while (1):
						current_letter = source_file.read(1)
						if current_letter == '\n':
							line += 1
						next_letter = peek_next_letter()
						if current_letter == "\n":
							try:
								current_tk.remove("/")
								current_tk.remove("/")
							except:
								pass
							break
			try:	
				current_tk.remove(current_letter)
				current_tk.remove(next_letter)
			except:
				pass

		# Check NUM_OP: (1-character operator always)
		if (current_letter in NUM_OP):
			current_tk.append(current_letter)
			return joined(current_tk), NUM_OP.get(joined(current_letter)) # current_tk not current_letter
		
		# Check COMP_OP:
		if current_letter in COMP_OP:
			current_tk.append(current_letter)
			current_tk.append(next_letter)
			# 2-characters COMP_OP:
			if (joined(current_tk) in COMP_OP):
				source_file.seek(source_file.tell()+1)
				return joined(current_tk), COMP_OP.get(joined(current_tk))
			# 1-character COMP_OP:	
			else:
				current_tk.remove(next_letter)
				return joined(current_tk), COMP_OP.get(joined(current_tk))
					
		# Check ASSIGN_OP and SEPERATOR:
		if current_letter in SEPERATOR:
			if current_letter == ':':
				current_tk.append(current_letter)
				current_tk.append(next_letter)
				if (joined(current_tk) in ASSIGN_OP):
					source_file.seek(source_file.tell()+1)
					return joined(current_tk), ASSIGN_OP.get(joined(current_tk)) 
			#else:
				current_tk.remove(current_letter)
				current_tk.remove(next_letter)
			current_tk.append(current_letter)
			return joined(current_tk), SEPERATOR.get(joined(current_tk))

		# Check GROUP_OP:
		if current_letter in GROUP_OP:
			current_tk.append(current_letter)
			return joined(current_tk), GROUP_OP.get(joined(current_tk))

		# Check ID, KEYWORDS
		try:
			if (current_letter.isalpha() or current_tk[-1].isalpha()):
				current_tk.append(current_letter)
				if (not next_letter.isalpha() and not next_letter.isdigit()):
					if (joined(current_tk) in KEYWORDS):
						return joined(current_tk), KEYWORDS.get(joined(current_tk))
					return joined(current_tk), "id_tk"
		except IndexError:
			if (current_letter.isalpha()):
				current_tk.append(current_letter)
				if (not next_letter.isalpha() and not next_letter.isdigit()):
					if (joined(current_tk) in KEYWORDS):
						return joined(current_tk), KEYWORDS.get(joined(current_tk))
					return joined(current_tk), "id_tk"

		# Check INTEGER:
		if (current_letter.isdigit()):
			current_tk.append(current_letter)
			if (not next_letter.isdigit() and not next_letter.isalpha()):
				if ( not (int(joined(current_tk)) >= -32767 and int(joined(current_tk)) > 32767)):
					return joined(current_tk), "integer_tk"
				else:
					error_handler("Integer values should be between -32767 and 32767")
			elif (next_letter.isalpha()):
				error_handler("(LEX): Identifier names should start with a letter.") 
				sys.exit(1)
					
	return 0,0  # for debug reasons

# Symbol Table: -------------------------------------------------------------------------

# General Definitons:

scope_list = []

# Entity types:

class entity():
	name = ""
	in_scope = None
	entity_type = "generic_entity_type"
	def __init__(self, name, entity_type):
		self.name = name
		self.entity_type = entity_type

	def set_scope(self, scope):
		self.in_scope = scope

	def __str__(self):
		return "name: " + str(self.name) 

class variable(entity):
	offset = -1
	variable_type = "int" # TODO
	def __init__(self, name, offset):
		super().__init__(name, "variable_type")
		self.offset = offset

	def __str__(self):
		return super().__str__() + " offset: " + str(self.offset)

class function(entity):
	start_quad = -1
	argument = []
	framelength = -1
	function_type = "function" # Type = function/procedure
	def __init__(self, name):
		super().__init__(name, "function_type")

	def new_argument(self, new_argument):
		self.argument.append(new_argument)

	def update_start_quad(self, quad):
		self.start_quad = quad

	def update_framelength(self, flength):
		self.framelength = flength

	def __str__(self):
		return super().__str__() + " start_quad: " + str(self.start_quad) + " argument: " + str(self.argument) + " framelength: " + str(self.framelength)

class constant(entity):
	value = 0
	def __init__(self, name, value):
		super.__init__(name, "constant_type")
		self.value = value
	def __str__(self):
		return super().__str__() + " value: " + str(self.value)

class parameter(entity):
	par_mode = "" # in / inout
	offset = -1
	name = ""
	def __init__(self, name, par_mode, offset):
		super().__init__(name, "parameter_type")
		self.name = name
		self.par_mode = par_mode
		self.offset = offset

	def __str__(self):
		return super().__str__() + " par_mode: " + str(self.par_mode) + " offset: " + str(self.offset)

class temp_variable(entity):
	offset = -1
	def __init__(self, name, offset):
		super().__init__(name, "temp_variable_type")
		self.offset = offset

	def __str__(self):
		return super().__str__() + " offset: " + str(self.offset)

# Scope:

class scope():
	list_entity = []
	nesting_level = -1
	offset = 12
	def __init__(self, list_entity, nesting_level):
		self.list_entity = list_entity
		self.nesting_level = nesting_level
	def __str__(self):
		return "nesting_level: " + str(self.nesting_level) + "Entity List: " + str(self.list_entity)

	def add_entity(self, entity):
		self.list_entity.append(entity)

	def update_offset(self, x):
		current_offset = self.offset
		self.offset += x
		return current_offset

# Argument:

class argument(): # for function entity
	par_mode = ""
	arg_type = ""
	def __init__(self, par_mode, arg_type):
		self.par_mode = par_mode
		self.arg_type = arg_type
	def __str__(self):
		return "par_mode: " + str(self.par_mode) + " var_type: " + str(self.var_type)

# Symbol Table Actions: ---------------------------------------------------------

def search_for_entity_str(str_name, switch = False):
	i = -1
	if len(scope_list) > 0:
		try:
			while ((scope_list[i] != None) and (i >= -(len(scope_list)))): 
				for an_entity in scope_list[i].list_entity: 
					if an_entity.name == str_name:
						if switch == True:
							return an_entity, scope_list[i].nesting_level
						return an_entity
				i -= 1
		except IndexError:
			warning_handler("[search_for_entity_str] Entity " + str(str_name) + " not declared")
			return None
	return None


def search_for_entity(entity_name, ent_type, switch = False):
	i = -1
	if len(scope_list) > 0:
		try:
			while ((scope_list[i] != None) and (i >= -(len(scope_list)))): # OutOfBounds Error??
				for an_entity in scope_list[i].list_entity: 
					if an_entity.name == entity_name and an_entity.entity_type == ent_type:
						if switch == True:
						#	print(an_entity.name)
						#	print(scope_list[i].nesting_level)
							return an_entity, scope_list[i].nesting_level
						return an_entity
				i -= 1
		except IndexError:
			return None
	return None

def check_redefinition(entity, which_scope):
	entity_name = entity.name
	entity_type = entity.entity_type
	scope = scope_list[which_scope]
	for ent in scope.list_entity:
		if ent.entity_type == entity_type and ent.name == entity_name:
			return True
	return False

def check_redefinition_name_only(entity, which_scope):
	entity_name = entity.name
	scope = scope_list[which_scope]
	for ent in scope.list_entity:
		if ent.name == entity_name:
			return True
	return False

# SCOPE Actions: -----------------------------------------------------------------

def add_scope():
	if len(scope_list) == 0:
		new_scope = scope([],0)
	else:
		new_scope = scope([],((scope_list[-1].nesting_level)+1))
	scope_list.append(new_scope)

def delete_scope():
	try:
		del_scope = scope_list[-1]
	except IndexError:
		warning_handler("[INFO] (delete_scope): No scope to remove.")
		return
	scope_list.remove(del_scope)

# ENTITY Actions: ------------------------------------------------------------------

def add_variable_entity(name): 
	var_offset = scope_list[-1].update_offset(4) # make some room for a new variable
	new_entity = variable(name, var_offset)
	redefined = check_redefinition(new_entity, (-1))
	redefined_name = check_redefinition_name_only(new_entity, (-1))
	if redefined or redefined_name:
		error_handler("Redefinition of variable " + str(name))
	new_entity.set_scope(scope_list[-1].nesting_level)
	scope_list[-1].add_entity(new_entity)

def add_temp_variable_entity(name):
	temp_var_offset = scope_list[-1].update_offset(4)
	new_entity = temp_variable(name, temp_var_offset)
	new_entity.set_scope(scope_list[-1].nesting_level)
	scope_list[-1].add_entity(new_entity)

def add_function_entity(name): 
	new_entity = function(name)
	redefined = check_redefinition(new_entity, (-2))
	if redefined:
		error_handler("Redefinition of function " + str(name))
	#new_entity.set_scope(scope_list[-2].nesting_level)
	new_entity.set_scope(scope_list[-1].nesting_level)
	scope_list[-2].add_entity(new_entity)

def add_parameter_entity(name, par_mode): # for scope
    par_offset = scope_list[-1].update_offset(4)
    new_entity = parameter(name, par_mode, par_offset)
    new_entity.set_scope(scope_list[-1].nesting_level) 
    redefined = check_redefinition(new_entity, (-1))
    if redefined:
    	error_handler("Redefinition of parameter " + str(name))
    scope_list[-1].add_entity(new_entity)
    return new_entity

def add_argument_entity(par_mode): 
	# Does not add anything anywhere, just generates and returns an argument instead					
	if par_mode == "in":
		mode = "CV"
	else:
		mode = "REF"
	new_entity = argument(par_mode, "int")
	return new_entity

# FUNTION ENTITY Actions: -----------------------------------------------------------

def function_entity_change_quad(name, new_quad):
	global program_name
	if name == program_name:
		return 
	function_entity = search_for_entity(name, "function_type")
	function_entity.update_start_quad(new_quad)
	return new_quad

def function_entity_change_framelength(name, new_framelength):
	function_entity = search_for_entity(name, "function_type")
	function_entity.framelength = new_framelength

def function_entity_add_argument(function_name, argument): # argument, for function
	try:
		function_entity = search_for_entity(function_name, "function_type")
	except:
		error_handler("Function " + str(function_name)+" not declared in Symbol Table")
	function_entity.new_argument(argument)

# DEBUGGING: Print Scope and Entities (currently without their offset in order to be generic for both vars and funcs):

def print_symbol_table():
	print("Printing Scopes and their entities:\n")
	for scope in scope_list:
		print("SCOPE " + str(scope.nesting_level) +" has:")
		if len(scope.list_entity) != 0:
			for entity in scope.list_entity:
				if entity.entity_type == "function_type":
					print("ENTITY: " + str(entity.name) + " OF TYPE " + str(entity.entity_type) + " START_QUAD " + str(entity.start_quad) + " FRAMELENGTH " + str(entity.framelength))
				else: 
					print("ENTITY: " + str(entity.name) + " OF TYPE " + str(entity.entity_type) + " OFFSET " + str(entity.offset)) #+ offset
		print('-----------\n\n')

# Intermediate code: ------------------------------------------------------------------

quad_label = 0		# Note: quad_label is an integer >=1, not a str (like L1:..., L2:,...,etc)
quad_list = []
tempvar_counter = -1 # could be initialized to 0 too.

class quad():
	label = ""
	op = ""
	x = ""
	y = ""
	z = ""
	def __init__(self, label, op, x, y, z):
		self.label = str(label)
		self.op = str(op)
		self.x = str(x)
		self.y = str(y)
		self.z = str(z)

	def __str__(self): # For printing class elements in python...
		return str(self.label)+":\t"+str(self.op)+" "+str(self.x)+" "+str(self.y)+" "+str(self.z)

def genquad(op, x, y, z): 
	global quad_list, quad_label
	quad_label += 1
	label = quad_label
	new_quad = quad(label, op, x, y, z)
	quad_list.append(new_quad)
	return new_quad

def nextquad():
	global quad_label
	return quad_label+1

def newtemp(): 
	global tempvar_counter
	tempvar_counter += 1
	tempvar = "T_"+str(tempvar_counter)
	return tempvar

def emptylist():
	return []

def makelist(x):
	return [x]

def merge(list1, list2):
	return list1 + list2 

def backpatch(l, z): # Fixed, needed an int() cast...
	global quad_list
	for a_quad in quad_list:
		if int(a_quad.label) in l:
			a_quad.z = z

def print_quads():
	for quad in quad_list:
		print(quad)

def write_intermediate_code_tofile():
	try:
		int_file = "intermediate_code.int"
		out_file = open("intermediate_code.int","w+")
		print("[INFO]\tWriting Intermediate code to file "+"<"+int_file+">")
	except FileNotFoundError:
		print("Could not open file: 'intermediate_code.int'. \nContinue without writing the intermediate code to file? (y/n)?")
		while (1):
			cont = input()
			if cont == "y" or cont == "Y":
				return
			elif cont == "n" or cont == "N":
				print("Exiting...")
				sys.exit()
			else:
				print("Could not open file: 'intermediate_code.int'. \nContinue without writing the intermediate code to file? (y/n)?")
	
	for q in quad_list:
		out_file.write(str(q)+'\n')
	out_file.close()

def generate_c_code(outfile):
	global quad_list
	global program_name
	try:
		out_file = open(outfile, "w+")
	except FileNotFoundError:
		error_handler("Could not open out_file to write the C intermediate code, exiting...")
	print("[INFO]\tWriting C code to file "+"<"+outfile+">")

	line_counter = 0

	def write_label():
		out_file.write("L"+str(line_counter)+":; ")
	
	def write_include():
		out_file.write("#include <stdio.h>\n")

	def declare_vars():
		for var in variables_to_declare:
			out_file.write("\tint "+str(var)+";\n")

	variables_to_declare = set()
	for q in quad_list:
		if q.op == ":=" or q.op in NUM_OP:
			try:
				is_int_x = int(q.x)
			except ValueError:
				variables_to_declare.add(q.x)
			try:
				is_int_z = int(q.z)
			except ValueError:
				variables_to_declare.add(q.z)
		elif q.op in COMP_OP:
			try:
				is_int_x = int(q.x)
			except ValueError:
				variables_to_declare.add(q.x)
			try:
				is_int_y = int(q.y)
			except ValueError:
				variables_to_declare.add(q.y)

	# Begin the translation of the saved quads in C code:
	write_include()
	call_warning_flag = True
	for q in quad_list:
		line_counter += 1
		if q.op == "begin_block":
			if q.label == "1": 		# The first quad has the program's name
				out_file.write("int main() {\n")
				declare_vars() 		# After the main() function, declare
									# all int variables found in the quad_list
			else:
				out_file.write(str(q.x)+":;")
				out_file.write("\tint "+q.x+"("+")"+"{\n") 

		elif q.op == "end_block":
			if q.x != quad_list[0].x: # Check if the block refers to main() function
				out_file.write("}\n") # If not, write a '}' (without 'return 0')
			else:
				out_file.write("\n")  # skip this

		elif q.op == "halt":
			write_label()
			out_file.write("\treturn 0; \n}") 

		elif q.op == "par": # Could print a warning here too, but would cause some bloat in info messages.
			pass
		elif q.op == "call":# Print a warning, the C code doesn't support functions.
			if call_warning_flag:
				warning_handler("Source file contains function(s). The C Code generated by the Compiler will not work properly.")
				return
			call_warning_flag = False

		elif q.op == "RET":	
			write_label()
			out_file.write("\treturn "+q.x+";\n")

		elif q.op == ":=":
			write_label()
			if q.z.isdigit():
				out_file.write("\t"+q.x+" = "+q.z+";\n")	
			else:
				out_file.write("\t"+q.z+" = "+q.x+";\n")

		elif q.op in COMP_OP: 
			write_label()
			# Change the minimal++ operator (q.op) to a C operator (c_op)
			if q.op == "=":
				c_op = "=="
			elif q.op == "<>":
				c_op == "!="
			else:
				c_op = q.op
			# Then write to file the appropriate expression:
			if q.z != "_" or q.z != None: 	# If q.z exists, it's an if statement:
				out_file.write("\tif ("+q.x+" "+c_op+" "+q.y+"){ goto "+"L"+str(q.z)+"; }\n")
			else: 						  	# Otherwise, it's a comparison:
				out_file.write("\t"+q.x+" "+c_op+" "+q.y+";\n")

		elif q.op in NUM_OP:
			write_label()
			out_file.write("\t"+q.z+" = "+q.x+" "+q.op+" "+q.y+";\n")

		elif q.op == "out":
			write_label()
			out_file.write("\tprintf(\"%d\\n\","+q.x+");\n")

		elif q.op == "jump":
			write_label()
			out_file.write("\tgoto L"+str(q.z)+";\n")
		
	out_file.close()

# SYN [and Quads]: ----------------------------------------------------------------

token_and_value = []
token = None
token_value = None

def get_next_token():
	global token_value, token, token_and_value
	token_and_value = lex()
	token = token_and_value[1]
	token_value =  token_and_value[0]

program_name = ""
main_framelength = -1
def syn():
	# For syntax analysis:
	global token, token_value, token_and_value
	global program_name

	# For intermediate code:
	global quad_list
	global scope_list
	def program():
		global program_name
		if token == "keyword-program_tk":
			get_next_token()
			if token == "id_tk":
				block_name = token_value
				program_name = token_value
				add_scope()
				get_next_token()
				block(block_name)
				print("[SYN]\tSyntax analysis of the program completed successfully." )
			else:
				error_handler("Expected <program-name> after 'program'")
		else:
			error_handler("Expected 'program' keyword at the begining of the source file.")

	def block(block_name):
		global program_name, main_framelength, program_start_quad, quad_list
		declarations()	
		subprograms()
		if block_name == program_name:
			block_start_quad = nextquad()-1
		else:
			block_start_quad = function_entity_change_quad(block_name, nextquad()-1)
		genquad("begin_block", block_name, "_", "_")
		statements()
		if block_name == program_name:
			genquad("halt", "_", "_", "_")
		genquad("end_block", block_name, "_", "_")
		if block_name != program_name:
			function_entity_change_framelength(block_name, scope_list[-1].offset) # Handle with care, raises AttributeError
		else:
			main_framelength = scope_list[0].offset 
		#print_symbol_table()
		for quad in (quad_list[block_start_quad:]):
			generate_final_code(quad, block_name)
		if program_name != block_name:
			delete_scope()

	def declarations():
		while token == "keyword-declare_tk":
			get_next_token()
			varlist()
			if token == "semicolon_tk":
				get_next_token() # success!
			else:
				error_handler("Expected ; after declarations")

	def varlist():
		if token == "id_tk":
			add_variable_entity(token_value)
			get_next_token()
			while token == "comma_tk":
				get_next_token()
				if token == "id_tk":
					add_variable_entity(token_value)
					get_next_token()
				else:
					error_handler("Expected ID after <comma>")

	def subprograms():
		while (token == "keyword-function_tk" or token == "keyword-procedure_tk"):
			get_next_token()
			subprogram()

	def subprogram():
		if token == "id_tk":
			block_name = token_value
			add_scope()
			add_function_entity(block_name)
			get_next_token()
			funcbody(block_name)
		else:
			error_handler("Expected subprogram ID (subprogram name)")

	def funcbody(block_name):
		formalpars(block_name)
		block(block_name)

	def formalpars(block_name):
		if token == "open-paren_tk":
			get_next_token()
			formalparlist(block_name)
			if token == "close-paren_tk":
				get_next_token() # success
				return
			else:
				error_handler("Expected ')' symbol after subprogram parameters")

	def formalparlist(block_name):
		formalparitem(block_name)
		while token == "comma_tk":
			get_next_token()
			if token == "keyword-in_tk" or token == "keyword-inout_tk":
				formalparitem(block_name)
			else:
				error_handler("Expected keyword 'in' or 'inout' in subprogram's parameters")

	def formalparitem(block_name): 
		if token == "keyword-in_tk" or token == "keyword-inout_tk":
			par_mode = token_value
			get_next_token()
			if token == "id_tk":
				par_name = token_value
				arg = add_argument_entity(par_mode)
				add_parameter_entity(par_name, arg.par_mode)
				function_entity_add_argument(block_name, arg)
				get_next_token() # success
				return
			else:
				error_handler("Expected Identifier after <in/inout> keyword")

	def statements():
		if token == "open-hook_tk":
			get_next_token()
			statement()
			while token == "semicolon_tk":
				get_next_token()
				statement()
			if token == "close-hook_tk":
				get_next_token() # success
				return
			else: 
				print(token_value)
				error_handler("Expected ';' after a statement.")
			get_next_token()
		else:
			statement()
			if token == "semicolon_tk":
				get_next_token()
			else:
				error_handler("Expected ';' after a single statement!")

	def statement():
		if token == "id_tk":
			before_assign_op = token_value
			after_assign_op = assignment_stat()
			# Support for function-result assignmets, ex: x := f(y);
			try: 
				entity_exists = search_for_entity(after_assign_op, "function_type")
				if entity_exists.name == after_assign_op: # assignment is: [x := function result]
					w = newtemp()
					add_temp_variable_entity(w)
					genquad("par", w, "RET", "_")
					genquad("call", after_assign_op, "_", "_")
					genquad(":=", w, "_", before_assign_op)
			except:
				# this should be generated as default:
				genquad(":=", after_assign_op, "_", before_assign_op)
		if_stat()
		while_stat() 
		doublewhile_stat() 
		loop_stat() 
		forcase_stat() 
		exit_stat() 
		incase_stat()
		call_stat() 
		return_stat()
		input_stat() 
		print_stat() 
		
	def assignment_stat():
		to_return = None # 0.3.5
		if token == "id_tk":
			try:
				res = search_for_entity_str(token_value)
			except:
				error_handler("Variable "+str(token_value)+" not declared")

			get_next_token()
			if token == "assign-op_tk":
				get_next_token()
				to_return = expression()
				if token != "semicolon_tk":
					error_handler("Expected ';' after expression")
		return to_return

	def if_stat():
		if token == "keyword-if_tk":
			get_next_token()
			if token == "open-paren_tk":
				get_next_token()
				[b_true, b_false] = condition()
				if token == "close-paren_tk":
					get_next_token()
					if token == "keyword-then_tk":
						backpatch(b_true, nextquad())
						get_next_token()
						statements()
						if_list = makelist(nextquad())
						genquad("jump", "_", "_", "_")
						backpatch(b_false, nextquad())
						# accept None statements? (currently yes)
						elsepart()
						backpatch(if_list, nextquad())
					else:
						error_handler("Expected 'then' after 'if'")
				else:
					error_handler("Expected ')' after 'if'")
			else:
				error_handler("Expected '(' after 'if'")

	def elsepart():
		if token == "keyword-else_tk":
			get_next_token()
			statements()

	def while_stat():
		if token == "keyword-while_tk":
			b_quad = nextquad()
			get_next_token()
			if token == "open-paren_tk":
				get_next_token()
				[b_true, b_false] = condition()
				if token == "close-paren_tk":
					get_next_token() 
					backpatch(b_true, nextquad())
					statements()
					genquad("jump", "_", "_", b_quad)
					backpatch(b_false, nextquad())
				else:
					error_handler("Expected ')' after while statements")
			else:
				error_handler("Expected '(' after 'while' keyword")

	def doublewhile_stat(): # Cancelled
		if token == "keyword-doublewhile_tk":
			state = newtemp()
			add_temp_variable_entity(state) #0.4
			genquad(":=", "0", "", state)
			condquad = nextquad()
			get_next_token()
			if token == "open-paren_tk":
				get_next_token()
				[cond_true, cond_false] = condition()
				backpatch(cond_true, nextquad())
				state1_list = makelist(nextquad())
				genquad("=", "2", state, "_")
				genquad(":=", "1", "", state)
				if token == "close-paren_tk":
					get_next_token()
					statements()
					genquad("jump", "", "", condquad)
					if token == "keyword-else_tk":
						backpatch(cond_false, nextquad())
						state2_list = makelist(nextquad())
						genquad("=", "1", state, "_")
						genquad(":=", "2", "", "_")

						get_next_token()
						statements()

						genquad("jump", "", "", condquad)
						backpatch(state1_list, nextquad())
						backpatch(state2_list, nextquad())
					else:
						error_handler("Expected 'else' after doublewhile statements")
				else:
					error_handler("Expected ')' after doublewhile statements")
			else:
				error_handler("Expected '(' after doublewhile keyword")

	def loop_stat(): # Cancelled
		if token == "keyword-loop_tk":
			get_next_token()
			statements()

	def exit_stat(): # Cancelled
		if token == "keyword-exit_tk":
			get_next_token() # success!

	def forcase_stat(): 
		if token == "keyword-forcase_tk":
			b_quad = nextquad()
			get_next_token()
			while (token == "keyword-when_tk"):
				get_next_token()
				if token == "open-paren_tk":
					get_next_token()
					[b_true, b_false] = condition()
					print(token_value)
					if token == "close-paren_tk":
						get_next_token()
						print(token_value)
						if token == "colon_tk":
							get_next_token()
							backpatch(b_true, nextquad())
							statements()
							genquad("jump","_","_",b_quad)
						else:
							error_handler("Expected ':' token after <when> (<condition>) in <forcase>")
					else:
						error_handler("Expected ')' after <when> in <forcase> ")
				else:
					error_handler("Expected '(' after <when> in forcase")
			if token == "keyword-default_tk":
				get_next_token()
				if token == "colon_tk":
					get_next_token()
					
					statements()
					backpatch(b_false, nextquad())
				else:
					error_handler("Expected ':' after 'default' keyword.")
			else: 
				error_handler("Expected 'default' action after 'forcase'.")

	def incase_stat(): # Cancelled
		if token == "keyword-incase_tk":
			t = newtemp()
			add_temp_variable_entity(t) #0.4
			first_quad = nextquad()
			genquad(":=", '0', '_', t)
			get_next_token()
			while token == "keyword-when_tk":
				if token == "open-paren_tk":
					get_next_token()
					[cond_true, cond_false] = condition()
					backpatch(cond_true, nextquad())
					if token == "close-paren_tk":
						get_next_token()
						if token == "colon_tk":
							get_next_token()
							statements()
							genquad(":=", '1', "_", t)
							backpatch(cond_false, nextquad())
						else:
							error_handler("Expected ':' after <when> (condition) in incase")
					else:
						error_handler("Expected ')' after <when> in incase")
				else:
					error_handler("Expected '(' after <when> in incase_stat")

	def return_stat():
		if token == "keyword-return_tk":
			get_next_token()
			e = expression()
			# Handle return(function()) types of return:
			try:
				entity_exists = search_for_entity(e, "function_type")
				if entity_exists.name == e:
					w = newtemp()
					add_temp_variable_entity(w)
					genquad("par", w, "RET", "_")
					genquad("call", e, "_", "_")
					genquad("retv", w, "_", "_")

			except: # this should be generated as default
				genquad("retv", e, "_", "_")

	def call_stat():
		if token == "keyword-call_tk":
			get_next_token()
			if token == "id_tk":
				callee = token_value
				get_next_token()
				actualpars()
				genquad("call", callee, "_", "_")

	def print_stat():
		if token == "keyword-print_tk":
			get_next_token()
			if token == "open-paren_tk":
				get_next_token()
				e = expression()
				genquad("out", e, "_", "_")
				if token == "close-paren_tk":
					get_next_token() # success!
					return
				else:
					error_handler("Expected ')' token after print()")
			else:
				error_handler("Expected '(' token after print()")

	def input_stat():
		if token == "keyword-input_tk":
			get_next_token()
			if token == "open-paren_tk":
				get_next_token()
				if token == "id_tk":
					input_value = token_value
					get_next_token()
					if token == "close-paren_tk":
						genquad("inp",input_value,"_", "_")
						get_next_token() # success!
						return
					else:
						error_handler("Expected ')' after input()")
				else:
					error_handler("Expected ID inside input(<ID>)")
			else:
				error_handler("Expected '(' after input ")

	def actualpars():
		if token == "open-paren_tk":
			get_next_token()
			actualparlist()
			if token == "close-paren_tk":
				get_next_token() # success!
				return
			else:
				error_handler("Expected ')' after <parameters>")

	def actualparlist():
		actualparitem()
		while token == "comma_tk":
			get_next_token() 
			actualparitem()

	def actualparitem():
		if token == "keyword-in_tk":
			get_next_token()
			e = expression()
			genquad("par", e, "CV", "_")
		elif token == "keyword-inout_tk":
			get_next_token()
			parameter = token_value
			genquad("par", parameter, "REF", "_")
			if token == "id_tk":
				get_next_token() # success!
				return
			else:
				error_handler("Expected ID after <inout> keyword")

	def condition():
		[b_true, b_false] = [q1_true, q1_false] = boolterm()
		while token == "keyword-or_tk":
			backpatch(b_false, nextquad())
			get_next_token()
			[q2_true, q2_false] = boolterm()
			b_true = merge(b_true, q2_true)
			b_false = q2_false
		return [b_true, b_false]

	def boolterm():
		[q_true, q_false] = [r1_true, r1_false] = boolfactor()
		while token == "keyword-and_tk":
			backpatch(q_true, nextquad())
			get_next_token()
			[r2_true, r2_false] = boolfactor()
			q_false = merge(q_false, r2_false)
			q_true = r2_true
		return [q_true, q_false]			

	def boolfactor():
		if token == "open-bracket_tk":
			get_next_token()
			to_return = condition()
			if token == "close-bracket_tk":
				get_next_token() # success!
				return
			else:
				error_handler("Expected ']' after opening '['")
		elif token == "keyword-not_tk":
			get_next_token()
			if token == "open-bracket_tk":
				get_next_token()
				to_return = condition()
				to_return = to_return.reverse() # revert list as the not-rule suggests
				if token == "close-bracket_tk":
					get_next_token() # success!
					return
				else:
					error_handler("Expected ']' after opening '['")
			else:
				error_handler("Expected '[' after 'not' keyword")
		else:
			e1 = expression()
			op = relational_oper()
			e2 = expression()
			r_true = makelist(nextquad())
			genquad(op, e1, e2, "_")
			r_false = makelist(nextquad())
			genquad("jump", "_", "_", "_")
			to_return = [r_true, r_false]
		return to_return

	def expression():
		op = optional_sign()
		t1 = term(op)
		while token == "add-oper_tk":
			op = add_oper()
			t2 = term(op)
			w = newtemp()
			add_temp_variable_entity(w) #0.4
			if (op == "-" and token_value == "+") or (op == "+" and token_value == "-"): # fixes <x := x - 1> expressions
				t2 = "-"+str(t2)
			genquad(op, t1, t2, w)
			t1 = w
		return t1

	def term(optional_sign):
		f1 = factor(optional_sign)
		while token == "mul-oper_tk":
			op = mul_oper()
			w = newtemp()
			add_temp_variable_entity(w) #0.4
			f2 = factor(optional_sign)
			genquad(op, f1, f2, w)
			f1 = w
		return f1

	def factor(optional_sign):
		to_return = None # if None is returned, Huston, we have a problem.
		if token == "open-paren_tk":
			get_next_token()
			to_return = expression()
			if token == "close-paren_tk":
				get_next_token() # success!
				return to_return
			elif (token != ("mul-oper_tk") and token != ("add-oper_tk")):
				error_handler("Expected (+, -, *, /), found something else")
			else: 
				error_handler("Expected ')' after opening a '('")
		elif token == "id_tk":
			to_return = token_value
			get_next_token() 
			id_tail = idtail()
			if id_tail != None:
				w = newtemp()
				add_temp_variable_entity(w) #0.4
				genquad("par", w ,"RET", "_")
				genquad("call", to_return, "_", "_")
				to_return = w
		elif token == "integer_tk": # == constant
			to_return = token_value			
			get_next_token() # success!
			return to_return

		return to_return

	def idtail():
		to_return = actualpars()
		return to_return

	def relational_oper(): 
		if token_value in COMP_OP:
			to_return = token_value
			get_next_token() # success!
			return to_return

	def add_oper(): 
		to_return = None
		if token == "add-oper_tk":
			to_return = token_value
			get_next_token() # success!
			return to_return
		return to_return

	def mul_oper(): 
		to_return = None
		if token == "mul-oper_tk":
			to_return = token_value
			get_next_token() # success!
			return to_return
		return to_return

	def optional_sign():
		return add_oper()

	get_next_token()
	program()
	write_intermediate_code_tofile()
	generate_c_code("c_code.c")

# Final Code: ---------------------------------------------------------------------------

# Helper Functions:
#
# gnvlcode: Transfers the adress of a non-local 
# 			variable (entity_var) to register $t0
def gnvlcode(entity_var): 
	global asm_file
	try:
		var, var_level = search_for_entity(entity_var.name, entity_var.entity_type, True)
	except:
		error_handler("gnvlcode error: variable "+str(entity_var.name) +" not declared in Symbol Table")

	asm_file.write("\tlw $t0, -4($sp)\n")
	this_level = scope_list[-1].nesting_level
	i = this_level

	while i > var_level: 
		#print(color.DARKCYAN+"gnvlcode prints i > this_level-var_level "+str(i)+">"+str(this_level-var_level)+color.END)
		asm_file.write("\tlw $t0, -4($t0)\n")
		i -= 1
	asm_file.write("\taddi $t0, $t0, -"+str(var.offset)+"\n")
#
# loadvr: Transfer data from variable str_var
#		  to register
def loadvr(str_var, register): 
	global asm_file
	if str(str_var).isdigit():
		asm_file.write("\tli $" + str(register) + ", "+str(str_var)+"\n")
		return

	try:
		var, var_level = search_for_entity_str(str_var, True)
	except:
		error_handler("loadvr error: variable not declared in Symbol Table")

	this_level = scope_list[-1].nesting_level
	main_prog_level = scope_list[0].nesting_level
	if var.entity_type == "variable_type" and var_level == main_prog_level:
		asm_file.write("\tlw $"+str(register)+", -"+str(var.offset)+"($s0)\n")

	elif (var.entity_type == "variable_type" and var_level == this_level) or (var.entity_type == "parameter_type" and var.par_mode == "in" and this_level == var_level) or var.entity_type == "temp_variable_type":
		asm_file.write("\tlw $"+str(register)+", -"+str(var.offset)+"($sp)\n")

	elif var.entity_type == "parameter_type" and var.par_mode == "inout" and var_level == this_level:
		asm_file.write("\tlw $t0, -"+str(var.offset)+"($sp)\n")
		asm_file.write("\tlw $"+str(register)+", ($t0)\n")

	elif var_level < this_level and ((var.entity_type == "variable_type")  or (var.entity_type == "parameter_type" and var.par_mode == "in")):
		gnvlcode(var)
		asm_file.write("\tlw $"+str(register)+", ($t0)\n")

	elif var.entity_type == "parameter_type" and var.par_mode == "inout" and var_level < this_level:
		gnvlcode(var)
		asm_file.write("\tlw $t0, ($t0)\n")
		asm_file.write("\tlw $"+str(register)+", ($t0)\n")

	else:
		error_handler("loadvr error: Shouldn't reach here...")		
#
# storerv: Transfers data from register
#		   to memory (str_var)
def storerv(register, str_var): # OK
	global asm_file
	try:
		var, var_level = search_for_entity_str(str_var, True)
	except:
		error_handler("storerv error: variable not declared in Symbol Table")

	this_level = scope_list[-1].nesting_level
	main_prog_level = scope_list[0].nesting_level

	if var.entity_type == "variable_type" and var_level == main_prog_level:
		asm_file.write("\tsw $"+str(register)+", -"+str(var.offset)+"($s0)\n")

	elif (var.entity_type == "variable_type" or var.entity_type == "parameter_type" and var_level == this_level) or var.entity_type == "temp_variable_type":
		asm_file.write("\tsw $"+str(register)+", -"+str(var.offset)+"($sp)\n")

	elif (var.entity_type == "parameter_type" and var.par_mode == "inout" and var_level == this_level):
		asm_file.write("\tlw $t0, -"+str(var.offset)+"($sp)\n")
		asm_file.write("\tsw $"+str(register)+", ($t0)\n")

	elif (var.entity_type == "variable_type" or (var.entity_type == "parameter_type" and var.par_mode == "in" and var_level < this_level)):
		gnvlcode(var)
		asm_file.write("\tsw $"+str(register)+", ($t0)\n")

	elif var.entity_type == "parameter_type" and var.par_mode == "inout" and var_level < this_level:
		gnvlcode(var)
		asm_file.write("\tlw $t0, ($t0)\n")
		asm_file.write("\tsw $"+str(register)+" ($t0)\n")
		
# Final Code Generation ----------------------------------------------------------------------
def write_final_code_labels(quad):
	global asm_file
	asm_file.write("L"+str(quad.label)+":\n")

i_counter = -1
write_main_label = True
def generate_final_code(quad, block_name): #(block_name, quad):
	global asm_file, program_name, write_main_label, main_framelength,i_counter #, program_name

	write_final_code_labels(quad)
	if write_main_label:
		asm_file.write("\tj Lmain\n")
		write_main_label = False

	# Initialize (or reset) the parameter counter:
	if quad.op == "par":
		i_counter += 1
	else:
		i_counter = -1

	# Start final code generation:
	if quad.op == "jump":
		asm_file.write("\tb L" + str(quad.z)+"\n")

	elif quad.op in COMP_OP:
		loadvr(quad.x, "t1")
		loadvr(quad.y, "t2")
		if quad.op == "=":
			asm_file.write("\tbeq $t1, $t2, L"+str(quad.z)+"\n")#asm_file.write("\tbeq $t1, $t1, $t2, "+str(quad.z)+"\n")
		elif quad.op == ">":
			asm_file.write("\tbgt $t1, $t2, L"+str(quad.z)+"\n")
		elif quad.op == "<":
			asm_file.write("\tblt $t1, $t2, L"+str(quad.z)+"\n")
		elif quad.op == "<>":
			asm_file.write("\tbne $t1, $t2, L"+str(quad.z)+"\n")
		elif quad.op == ">=":
			asm_file.write("\tbgt $t1, $t2, L"+str(quad.z)+"\n")
		elif quad.op == "<=":
				asm_file.write("\tble $t1, $t2, L"+str(quad.z)+"\n")

	elif quad.op in ASSIGN_OP:
		loadvr(quad.x, "t1")
		storerv("t1", quad.z)

	elif quad.op in NUM_OP:
		loadvr(quad.x, "t1")
		loadvr(quad.y, "t2")
		if quad.op == "+":
			if (str(quad.y)).isdigit():
				asm_file.write("\taddi $t1, $t1, "+str(quad.y)+"\n")
			else:
				asm_file.write("\tadd $t1, $t1, $t2\n")
		elif quad.op == "-":
			if (str(quad.y)).isdigit():
				asm_file.write("\tsubi $t1, $t1, "+str(quad.y)+"\n")
			else:
				asm_file.write("\tsub $t1, $t1, $t2\n")
		elif quad.op == "*":
			if (str(quad.y)).isdigit():
				asm_file.write("\tmul $t1, $t1, "+str(quad.y)+"\n")
			else:
				asm_file.write("\tmul $t1, $t1, $t2\n")
		elif quad.op == "/":
			if (str(quad.y)).isdigit():
				asm_file.write("\tdiv $t1, $t1, "+str(quad.y)+"\n")
			else:
				asm_file.write("\tdiv $t1, $t1, $t2\n")
		storerv("t1", str(quad.z))

	elif quad.op == "out":
		asm_file.write("\tli $v0, 1\n")
		loadvr(quad.x, "a0")
		asm_file.write("\tsyscall\n")

	elif quad.op == "in":
		asm_file.write("\tli $v0, 5\n")
		asm_file.write("\tsyscall\n")
		storerv("v0", quad.x)

	elif quad.op == "retv":
		loadvr(quad.x, "t1")
		asm_file.write("\tlw $t0, -8($sp)\n")
		asm_file.write("\tsw $t1, ($t0)\n")
		#asm_file.write("\tmove $v0, $t1\n")

	elif quad.op == "par":
		# Find the current function framelength, level (or main's framelength, level if not in a function)
		if block_name != program_name:
			current_function, current_function_level = search_for_entity(block_name, "function_type", True)
			framelength = current_function.framelength
		else: 
			current_function_level = 0
			framelength = main_framelength
		asm_file.write("\taddi $fp, $sp, "+str(framelength)+"\n")
		if quad.y == "CV":
			loadvr(quad.x, "t0")
			temp_i_offset = 4*i_counter + 12
			asm_file.write("\n\tsw $t0, -"+str(temp_i_offset)+"($fp)\n")
		elif quad.y == "REF":
			temp_i_offset = 4*i_counter + 12
			entity_x, x_level = search_for_entity_str(quad.x, True)
			if current_function_level == x_level:
				if (entity_x.entity_type == "variable_type" or (entity_x.entity_type == "parameter_type" and entity_x.par_mode == "in")):
					asm_file.write("\taddi $t0, $sp, -"+str(entity_x.offset)+"\n")
					asm_file.write("\tsw $t0, -"+str(temp_i_offset)+"($fp)\n")
				elif (entity_x == "parameter_type" and entity_x.par_mode == "inout"):
					asm_file.write("\tlw $t0, -"+str(entity_x.offset)+"($sp)\n")
					asm_file.write("\tsw $t0, -"+str(temp_i_offset)+"($fp)\n")
			else:
				if (entity_x.entity_type == "variable_type" or (entity_x.entity_type == "parameter_type" and entity_x.par_mode == "in")):
					gnvlcode(entity_x)
					asm_file.write("\tsw $t0, -"+str(temp_i_offset)+"($fp)\n")
				elif (entity_x.entity_type == "parameter_type" and entity_x.par_mode == "inout"):
					gnvlcode(entity_x)
					asm_file.write("\tlw $t0, ($t0)\n")
					asm_file.write("\tsw $t0, -"+str(temp_i_offset)+"($fp)\n")
		elif quad.y == "RET":
			entity_x = search_for_entity_str(quad.x)
			asm_file.write("\taddi $t0, $sp, -"+str(entity_x.offset)+"\n")
			asm_file.write("\tsw $t0, -8($fp)\n")

	elif quad.op == "call":
		if block_name != program_name:
			caller_function, caller_function_level = search_for_entity(block_name, "function_type", True)
			framelength = caller_function.framelength
		else:
			caller_function_level = 0
			framelength = main_framelength
		callee_function, callee_function_level = search_for_entity(quad.x, "function_type", True)
		if caller_function_level == callee_function_level:
			asm_file.write("\tlw $t0, -4($sp)\n")
			asm_file.write("\tsw $t0, -4($fp)\n")
		else: 
			asm_file.write("\tsw $sp, -4($fp)\n")
		asm_file.write("\taddi $sp, $sp, "+str(framelength)+"\n") 
		asm_file.write("\tjal L"+str(quad.x)+"\n")
		asm_file.write("\taddi $sp, $sp, -"+str(framelength)+"\n") 

	elif quad.op == "begin_block": 
		if quad.x == program_name: # In main function, write Lmain label:
			asm_file.write("\nLmain:\n\n")
			asm_file.write("\tsw $ra, ($sp)\n")
			asm_file.write("\taddi $sp, $sp, "+str(main_framelength)+"\n")
			asm_file.write("\tmove $s0, $sp\n")
		else: 
			asm_file.write("L"+str(quad.x)+":\n")	
			asm_file.write("\tsw $ra, ($sp)\n")

	elif quad.op == "end_block":
		if quad.x != program_name:
			asm_file.write("\tlw $ra, ($sp)\n")
			asm_file.write("\tjr $ra\n")

	elif quad.op == "halt":
		asm_file.write("#syscall code 10 (program halt)\n\tli $v0, 10\n")
		asm_file.write("\tsyscall\n")

def main():
	global source_file, asm_file
	check_arguments()
	try:
		source_file = open(str(sys.argv[1]),'r')
		print("[INFO]\tOpening the source file...")
	except FileNotFoundError:
		error_handler("Could not find the specified source file.")
	if len(sys.argv) > 2:
		try:
			asm_file = open(str(sys.argv[2]), 'w+')
		except FileNotFoundError:
			error_handler("Could not open <outfile>")
	else:
		try:
			asm_file = open("out.asm", 'w+')
		except FileNotFoundError:
			error_handler("Could not open <outfile>")

	syn() 
	print("[INFO]\tWriting final code to <outfile>.asm")
	print(color.GREEN+"[DONE]\tThe program '"+str(sys.argv[1])+"' compiled successfully. :)"+color.END)
	asm_file.close()
	source_file.close()

	# For Debug reasons (Ignore the following comments)
	#print("Scopes and entities in main:")
	#print_symbol_table()
	
	'''
	# SYMBOL TABLE: TEST 1:
	add_scope()
	add_variable_entity("x")
	add_temp_variable_entity("x1")
	add_variable_entity("x2")
	add_temp_variable_entity("y")
	add_scope()
	add_variable_entity("z")
	add_variable_entity("z1")
	#delete_scope()
	#delete_scope()
	add_scope()
	add_variable_entity("x")
	add_variable_entity("y")
	print(search_for_entity("y"))
	print_symbol_table()
	'''
	'''
	# SYMBOL TABLE: TEST 2 (Functions)
	add_scope()
	add_function_entity("f")
	print_symbol_table()
	'''
	
	
	# Run lex
	'''
	count = 0
	while(1):
		print("LEX: ", lex())
		if (count > 30): # change as wished
			break
		count+=1
	'''
	#print("LEX returns: ",lex())
	#print("LEX returns: ",lex())
	#print("LEX returns: ",lex())
	#print("LEX returns: ",lex())
	#print("LEX returns: ",lex())
if __name__=="__main__":
	main() 
