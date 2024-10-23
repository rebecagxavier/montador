import sys

memory = ['00' for _ in range(256)]

inst1 = {
    "add": '8',
    "shr": '9',
    "shl": 'a',
    "not": 'b',
    "and": 'c',
    "or": 'd',
    "xor": 'e',
    "cmp": 'f',
    "ld": '0',
    "st": '1'
}

inst2 = {
    "jz": '51',
    "je": '52',
    "jez": '53',
    "ja": '54',
    "jaz": '55',
    "jae": '56',
    "jaez": '57',
    "jc": '58',
    "jcz": '59',
    "jce": '5a',
    "jcez": '5b',
    "jca": '5c',
    "jcaz": '5d',
    "jcae": '5e',
    "jcaez": '5f',
    "jmp": '40'
}

inst3 = {"data": '2', "jmpr": '3'}

regi = {"r0": '00', "r1": '01', "r2": '10', "r3": '11'}


def bintodec(n):
  return int(n, 2)


def conversao(n):
  if (n).startswith("0b"):
    conv = (n)[2:]
    conv = bintodec(conv)
    conv = hex(conv)[2:]
  elif (n).startswith("0x"):
    conv = (n)[2:]
  else:
    conv = int(n)
    conv = hex(conv)[2:]
  return conv


def conversao2(n):
  n = bintodec(n)
  n = hex(n)[2:]
  return n


def input_file(input, output, memoria):
  with open(input, 'r') as file:
    arq = file.read()
    arq = arq.replace(",", " ")
    entrada = arq.split()
  for i in range(len(entrada)):
    entrada[i] = entrada[i].replace(",", " ")
    entrada[i] = entrada[i].lower()
  i = 0
  j = 0
  info = ""
  inst = ""
  dado = ""

  while i < len(entrada):
    print(entrada[i])

    if entrada[i] in inst1:
      inst = inst1[entrada[i]]
      info = regi[entrada[i + 1]] + regi[entrada[i + 2]]
      info = conversao2(info)
      memoria[j] = inst + info
      i += 2

    elif entrada[i] in inst2:
      instrucao = inst2[entrada[i]]
      dado = entrada[i + 1]
      dado = conversao(dado)
      dado = dado.zfill(2)
      memoria[j] = instrucao
      memoria[j + 1] = dado
      j += 1
      i += 1

    elif entrada[i] == 'clf':
      memoria[j] = '60'

    elif entrada[i] == 'halt':
      memoria[j] = '40'
      tmp= hex(j)[2:]
      tmp = tmp.zfill(2)
      memoria[j + 1] = tmp 
      j += 1

    elif entrada[i] == 'swap':
      inst = inst1['xor']
      info = regi[entrada[i + 1]] + regi[entrada[i + 2]]
      info = conversao2(info)
      dado = regi[entrada[i + 2]] + regi[entrada[i + 1]]
      dado = conversao2(dado)
      memoria[j] = inst + info
      memoria[j + 1] = inst + dado
      memoria[j + 2] = inst + info
      i += 2
      j += 2

    elif entrada[i] == 'in' or entrada[i] == 'out':
      inst = '7'
      info = regi[entrada[i + 2]]
      tipo = '0' if entrada[i] == 'in' else '1'
      dado = '0' if entrada[i + 1] == 'data' else '1'
      info = conversao2(tipo + dado + info)
      memoria[j] = inst + info
      i += 2

    else:
      inst = inst3[entrada[i]]
      info = regi[entrada[i + 1]]
      info = conversao2(info)
      memoria[j] = inst + info
      if inst == '2':
        dado = entrada[i + 2]
        dado = conversao(dado)
        dado = dado.zfill(2)
        memoria[j + 1] = dado
        j += 1
        i += 1
      i += 1

    i += 1
    j += 1
  output_file(memoria, output)


def output_file(memoria, path):
  header = "v3.0 hex words addressed\n"
  with open(path, 'w') as file:
    file.write(header)
    for i in range(256):
      file.write(f'{i:02x}: ' + memoria[i] + "\n")


input = sys.argv[1]
output = sys.argv[2]
input_file(input, output, memory)
