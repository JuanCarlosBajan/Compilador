let for = 'for'
let if = 'if'
let digit = ['0'-'9']
let char = ['a'-'z']
let separator = '/s'
let integer = (digit)+
let decimal = integer (('.' (integer))?)|('.')
let identificador = ['a'-'z']+ 'xyz'
let ERRORid = ['a'-'z']+
let quote = '"'
let string = (quote) (['0'-'z']|('/'))+ (quote)
let ERRORunclosedstring = (quote) (['0'-'z']|('/'))+


rule tokens =
 digit	{print("digit")}
  | char	{ print("char") }
  | identificador	{ print("identificador") }
  | integer	{ print("integer") }
  | if	{ print("if") }
  | for	{ print("for") }
  | while	{ print("while") }
  | separator	{ print("separator") }
  | quote	{ print("quote") }
  | ERRORunclosedstring	{ print("ERRORunclosedstring") }
  | string	{ print("string") }