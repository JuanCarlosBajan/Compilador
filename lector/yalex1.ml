let digit = ['0'-'9']
let integer = (digit)+
let decimal = integer (('.' (integer))?)|('.')
let hexadecimal = ((digit)|['A'-'F'])+


rule tokens =
 digit	{print("digit")}
  | integer	{ print("integer") }
  | decimal	{ print("decimal") }
  | hexadecimal	{ print("hexadecimal") }