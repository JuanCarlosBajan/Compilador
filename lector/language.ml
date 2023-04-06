let digito = ['0'-'9']
let float = (digito)+ ('.' (digito)+)? ('E' ('/-'|'-')? (digito)+)?
let minuscula = ['a'-'z']

rule tokens =
	espacioEnBlanco	{}
  | identificador	{ print("Identificador\n") }
  | numero			{ print("Número\n") }
  | '+'				{ print("Operador de suma\n") }
  | '*'				{ print("Operador de multiplicación\n") }
  | '='				{ print("Operador de asignación\n") }