let separador = ('/n'|'/t'|'/s')
let openparenthesis = '('
let closeparenthesis = ')'
let closekey = '}'
let openkey = '{'
let equal = '='
let digito = ['0'-'9']
let int = (digito)+
let float = (int) ('.' (digito)+)? ('E' ('/-'|'-')? (digito)+)?
let var = 'var'
let def = 'def'
let quote = '"'
let char = ['a'-'z']
let identificador  = (char)+
#let ERRORunclosedstring = (quote) (identificador)
let string = (quote) (identificador) (quote)

rule tokens =
	espacioEnBlanco	{ WS }
  | digito	{ print("digito") }
  | separador { print("separador") }
  | openparenthesis { print("openparenthesis") }
  | closeparenthesis { print("closeparenthesis") }
  | closekey { print("closekey") }
  | openkey { print("openkey") }
  | equal { print("equal") }
  | float			{ print("float") }
  | int			{ print("int") }
  | var { print("var") }
  | def { print("def") }
  | char { print("char") }
  | identificador { print("identificador") }
  | ERRORunclosedstring { print("ERRORunclosedstring") }
  | string { print("string") }