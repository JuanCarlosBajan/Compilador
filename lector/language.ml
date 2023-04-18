let digito = ['0'-'9']
let float = (digito)+ ('.' (digito)+)? ('E' ('/-'|'-')? (digito)+)?
let var = 'var'
let def = 'def'
let char = ['a'-'z']
let identificador  = (char)+

rule tokens =
	espacioEnBlanco	{}
  | digito	{ print("digito\n") }
  | float			{ print("float\n") }
  | var { print("var\n") }
  | identificador { print("identificador\n") }
  | string { print("string\n") }