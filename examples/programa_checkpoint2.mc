:DECLARACOES
numero1:INTEIRO
numero2:INTEIRO
numero3:INTEIRO
aux:INTEIRO

:ALGORITMO
# Coloca 3 números em ordem crescente
LER numero1
LER numero2
LER numero3
SE numero1 > numero2 ENTAO
   INICIO
      aux = numero2
      numero2 = numero1
      numero1 = aux
   FIM 
SE numero1 > numero3 E numero2 <= numero4 E numero1 > 3 OU numero2 != numero4 ENTAO
   INICIO
      aux = (numero3)
      numero3 = numero1
      numero1 = aux
   FIM
SE numero2 > numero3 ENTAO
   INICIO
      aux = numero3
      numero3 = numero2
      numero2 = aux
   FIM
IMPRIMIR(numero1)
IMPRIMIR(numero2)
IMPRIMIR(numero3)
