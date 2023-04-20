let digit = ['0'-'9']
let integer = (digit)+
# para multiplicacion vamos a utilizar /x
let separator = '/s'
let multiply = '/x'
# para suma vamos a utilizar /-
let plus = '/-'
let minus = '-'
let divide = '/'
# dado que multiplicacion es /x utilizamos dos multiplicacion
let pow = '/x/x'
let if = 'if'
let for = 'for'
let while = 'while'
let char = ['a'-'z']
let identificador = (char)+


rule tokens =
 digit	{print("digit")}
  | multiply	{ print("multiply") }
  | integer	{ print("integer") }
  | plus	{ print("plus") }
  | minus	{ print("minus") }
  | divide	{ print("divide") }
  | pow	{ print("pow") }
  | if	{ print("if") }
  | for	{ print("for") }
  | while	{ print("while") }
  | separator	{ print("separator") }