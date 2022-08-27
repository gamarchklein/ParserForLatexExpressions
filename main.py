#Gabriel Marchioro Klein
#   Para  obter  os  pontos  relativos  a  este  trabalho,  você  deverá  fazer  um  programa,  usando  a 
# linguagem de programação que desejar, que seja capaz de validar expressões de lógica propisicional 
# escritas em latex e definir se são expressões gramaticalmente corretas. Você validará apenas a forma 
# da expressão (sintaxe).  
# A entrada será fornecida por um arquivo de textos que será carregado em linha de comando, 
# com a seguinte formatação:  
# 1. Na primeira linha deste arquivo existe um número inteiro que informa quantas expressões 
# lógicas estão no arquivo.  
# 2. Cada uma das linhas seguintes contém uma expressão lógica que deve ser validada.  
# A saída do seu programa será no terminal padrão do sistema e constituirá de uma linha de saída 
# para cada expressão lógica de entrada contendo ou a palavra valida ou a palavra inválida e nada mais. 
# Gramática:  
# Formula=Constante|Proposicao|FormulaUnaria|FormulaBinaria.  
# Constante="T"|"F". 
# Proposicao=[a−z0−9]+ 
# FormulaUnaria=AbreParen OperadorUnario Formula FechaParen 
# FormulaBinaria=AbreParen OperatorBinario Formula Formula FechaParen 
# AbreParen="(" 
# FechaParen=")" 
# OperatorUnario="¬" 
# OperatorBinario="∨"|"∧"|"→"|"↔" 
 
# Cada  expressão  lógica  avaliada  pode  ter  qualquer  combinação  das  operações  de  negação, 
# conjunção, disjunção, implicação e bi-implicação sem limites na combiação de preposições e operações. 
# Os valores lógicos True e False estão representados na gramática e, como tal, podem ser usados em 
# qualquer expressão de entrada. 
# Para  validar  seu  trabalho,  você  deve  incluir  no  repl.it,  no  mínimo  três  arquivos  contendo 
# números  diferentes  de  expressões  proposicionais.  O  professor  irá  incluir  um  arquivo  de  testes  extra 
# para validar seu trabalho. Para isso, caberá ao professor incluir o arquivo no seu repl.it e rodar o seu 
# programa carregando o arquivo de testes. 

import re

# gramatica:
Formula = ['Constante', 'Proposicao', 'FormulaUnaria', 'FormulaBinaria']
FormulaUnaria= ['AbreParen', 'OperatorUnario', 'Formula', 'FechaParen']
FormulaBinaria= ['AbreParen', 'OperatorBinario', 'Formula', 'Formula', 'FechaParen']
# terminais
Proposicao= re.compile(r'[a-z0-9]+')
Constante = ['T', 'F', 'True', 'False', True, False]
AbreParen = '('
FechaParen = ')'
OperatorUnario= '¬'
OperatorBinario= ['∨','∧','→','↔']
propNot = ['Formula','FormulaUnaria','FormulaBinaria','Proposicao','Constante','AbreParen','FechaParen','OperatorUnario', 'OperatorBinario'] # Pra resolver o problema que o regex criou
terminals = [Constante, AbreParen, FechaParen, OperatorUnario, OperatorBinario]


def varName(var):
 for name in globals():
     if eval(name) == var:
        return name

# Transforma os terminais em não-terminais
def firstParse(expression):
  try:
    args = expression.split(' ')
  except AttributeError:
    args = expression
  for i, arg in enumerate(args):
    for j, rule in enumerate(terminals):
      if arg in rule:
        args[i] = varName(terminals[j])
      elif Proposicao.search(arg) and arg not in propNot:
        args[i] = 'Proposicao'
  return args

# Transforma Constante e Preposicao em Formula
def secondParse(expression):
  args = firstParse(expression)
  for i, arg in enumerate(args):
    for j, rule in enumerate(Formula):
      if arg in rule:
        args[i] = 'Formula'
  return args

# Procura e transforma FormulaBinaria e FormulaUnaria em Formula
def thirdParse(expression):
  args = expression
  def innerParse(expression):
    args = secondParse(expression)
    newArgs = []
    openPar = 0
    for i, arg in enumerate(args):
      if arg == 'AbreParen':
        openPar += 1
        if args[i:i+4] == FormulaUnaria:
          newArgs.append('FormulaUnaria')
          del args[i:i+3]
          args[i] = 'FormulaUnaria'
        elif args[i:i+5] == FormulaBinaria:
          newArgs.append('FormulaBinaria')
          del args[i:i+4]
          args[i] = 'FormulaBinaria'
      elif arg == 'FechaParen':
        openPar -= 1
      elif openPar == 0:
        newArgs.append(arg)
    return args
  args = innerParse(args)
  if 'FormulaBinaria' in args or 'FormulaUnaria' in args:
    args = thirdParse(args)
  return args


def fourthParse(expression):
  args = thirdParse(expression)
  for i, arg in enumerate(args):
    for j, rule in enumerate(Formula):
      if arg in rule:
        args[i] = 'Formula'
  if args != ['Formula']:
    return False
  else:
    return True


def parseExpression(file):
  with open(file, 'r') as file:
    lines = file.readlines()
    stringNum = int(lines[0].strip())
    for i in range(1, stringNum + 1):
      try:
        line = lines[i].strip()
        if fourthParse(line) == True:
          print(f'{line}: válida')
        elif fourthParse(line) == False:
          print(f'{line}: inválida')
      except:
        print('Número de linhas registradas maior do que número de linhas presentes\n')
  file.close()

# Coloque seus arquivos de texto dentro das funções:
parseExpression('expression1.txt')
parseExpression('expression2.txt')
parseExpression('expression3.txt')