# Mini Compiler (Lexer) – Python

Lexer implementado em Python **sem comentários em código**, cobrindo os requisitos até o **Ponto 5**:

1. Identificadores: `(a-z|A-Z|_)(a-z|A-Z|_|0-9)*`
2. Operadores matemáticos: `+ - * /`
3. Atribuição: `=`
4. Operadores relacionais: `> >= < <= != ==`
5. Parênteses: `(` e `)`

Estrutura preparada para evoluir para os Pontos 6–9 posteriormente, mas **ainda não implementados** (números com ponto decimal, palavras reservadas, comentários, mensagens de erro já existem para léxicos não suportados; os recursos 6–8 estão apenas organizados para receber código).

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

## Observações para os Pontos 6–9 (a serem feitos depois)

- **Ponto 6 (números decimais)**: já existe `TokenType.NUMBER` e ganchos (`scan_number`) para implementar.
- **Ponto 7 (palavras reservadas)**: arquivo `keywords.py` com tabela; basta ligar a verificação em `scan_identifier`.
- **Ponto 8 (comentários)**: reservei métodos `skip_line_comment` e `skip_block_comment`, ainda não chamados.
- **Ponto 9 (erros com linha/coluna)**: já implementado para qualquer símbolo inválido.
