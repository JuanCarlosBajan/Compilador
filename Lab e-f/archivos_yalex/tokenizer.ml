let delim = ('/n'|'/t'|'/s')
let ws = delim+
let letter = ['a'-'z']
let digit = ['0'-'9']
let id = (letter)+
let plus = '/-'
let multiply = '/x'
let openparenthesis = '('
let closeparenthesis = ')'

rule tokens = 
  ws          { WS }
  | delim          { WS }
  | id        { ID }
  | plus      { PLUS }
  | multiply  { TIMES }
  | openparenthesis       { LPAREN }
  | closeparenthesis      { RPAREN }