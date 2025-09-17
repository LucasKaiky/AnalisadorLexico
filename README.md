# Mini Compiler (Lexer) – Python

Lexer implementado em Python **sem comentários em código**:

1. Identificadores: `(a-z|A-Z|_)(a-z|A-Z|_|0-9)*`
2. Operadores matemáticos: `+ - * /`
3. Atribuição: `=`
4. Operadores relacionais: `> >= < <= != ==`
5. Parênteses: `(` e `)`
6. Constantes numéricas com ponto decimal: válidos `123, 123.456, .456`, inválidos `1., 12., 156.`
7. Palavras reservadas: `int, float, print, if, else`
8. Comentários: `#` (linha única) e `/* ... */` (múltiplas linhas)
9. Erros léxicos: caracteres inválidos `(@, ``,`` ´, ç, ¨, etc, etc)` geram erro com linha e coluna


## Organização do projeto

```
mini_compiler_py/
  README.md
  examples/
    sample.mc
  src/
    minicompiler/
      __init__.py
      version.py
      tokens.py
      errors.py
      keywords.py
      lexer.py
      main.py
  tests/
    test_lexer_basic.py
```

## Executar

> Requer Python 3.10+ (sem dependências externas).

Opção 1 (simples):
```
cd src
python -m minicompiler.main ../examples/sample.mc
```

Opção 2 (rodar com um arquivo seu):
```
cd src
python -m minicompiler.main ../examples/seuarquivo.mc
```

A saída lista os tokens na ordem encontrados. Em caso de erro léxico (caracter não suportado ou números ainda não implementados), será mostrada mensagem com **linha:coluna**.

## Testes básicos

```
cd src
python -m unittest ../tests/test_lexer_basic.py -v
```

