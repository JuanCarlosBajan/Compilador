let separador = ('/n'|'/t'|'/s')
let openparenthesis = '('
let closeparenthesis = ')'
let closekey = '}'
let openkey = '{'
let equal = '='
let quote = '"'
let digito = ['0'-'9']
let int = (digito)+
let float = (int) ('.' (digito)+)? ('E' ('/-'|'-')? (digito)+)?
let var = 'var'
let def = 'def'
let char = ['a'-'z']
let identificador  = (char)+
let unclosedstring = (quote) (identificador)
let string = (quote) (identificador) (quote)

rule tokens =
	espacioEnBlanco	{}
  | digito	{ print("digito") }
  | separador { print("separador") }
  | openparenthesis { print("openparenthesis") }
  | closeparenthesis { print("closeparenthesis") }
  | closekey { print("closekey") }
  | openkey { print("openkey") }
  | equal { print("equal") }
  | float			{ print("float") }
  | var { print("var") }
  | def { print("def") }
  | char { print("char") }
  | identificador { print("identificador") }
  | unclosedstring { print("unclosedstring") }
  | string { print("string") }