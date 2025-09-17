# ================================
# 1) Identificadores
# Regra: (a-z | A-Z | _)(a-z | A-Z | _ | 0-9)*
# ================================
a
_b2
Var_123
x
y
z

# ================================
# 2) Operadores matemáticos: + - * /
# ================================
a+b-c*d/e

# ================================
# 3) Atribuição: =
# ================================
x = a
y = b
z = c

# ================================
# 4) Operadores relacionais: > >= < <= != ==
# ================================
x>y
x>=y
x<y
x<=y
x!=y
x==y

# ================================
# 5) Parênteses: ( )
# ================================
(a)
((x+y)*(z-(a/b)))

# ================================
# 6) Números com ponto decimal (válidos)
# Válidos: 123, 123.456, .456
# ================================
x = 123
y = 123.456
z = .456

# ================================
# 7) Palavras reservadas (devem ser reconhecidas como keywords)
# int, float, print, if, else
# ================================
int i
float f
print ( i )
if (i >= 0) else (f)

# ================================
# 8) Comentários (devem ser ignorados)
# Linha: começa com # até o fim da linha
# Bloco: /* ... */ pode ocupar várias linhas
# ================================
# isto é um comentário de linha
i = i + 1
/* bloco de comentário
   multi-linhas
   deve ser ignorado */
f = f / 2

# ================================
# 9) Erros léxicos (para demonstrar durante a apresentação)
# Descomente UMA linha por vez e execute para ver a mensagem "LexicalError: ... at linha:coluna"
# ================================

# 9.1) Numéricos inválidos terminando em ponto (devem falhar)
#1.
#12.
#156.

# 9.2) Caractere inválido
#@

# 9.3) '!' sozinho (sem '=' após)
#!

# 9.4) Bloco de comentário não encerrado
#/* comentário sem fechar

# 9.5) Outros caracteres não permitidos
#ç
#`

# Fim do arquivo de teste
