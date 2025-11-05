# Mini Compiler (Lexer/Parser) – Python

Compilador educacional em Python com:
- **Checkpoint 1 (Léxico)**: reconhece tokens básicos e reporta erros léxicos.
- **Checkpoint 2 (Sintaxe)**: valida a estrutura do código via parser recursivo-descendente.

> **Requer** Python **3.10+**. Sem dependências externas.

---

## ✨ Funcionalidades

### Checkpoint 1 — Léxico (itens 1–9)
1. **Identificadores**: `(a-z|A-Z|_)(a-z|A-Z|_|0-9)*`  
2. **Operadores matemáticos**: `+  -  *  /`  
3. **Atribuição**: `=`  
4. **Relacionais**: `>  >=  <  <=  !=  ==`  
5. **Parênteses**: `(` `)`  
6. **Números**: `123`, `123.456`, `.456`  
   - **Inválidos**: `1.`, `12.`, `156.`  
7. **Palavras reservadas (en)**: `int`, `float`, `print`, `if`, `else`  
8. **Comentários**: `#` (linha única) e `/* ... */` (múltiplas linhas)  
9. **Erros léxicos**: caracteres inválidos (ex.: `§`, `@`, `ç`, `¨`, …) com **linha:coluna**

### Checkpoint 2 — Sintaxe
- Parser **recursivo-descendente** com 1 método por não-terminal.
- Mensagens claras de erro sintático (**o que esperava**, **o que encontrou**, **linha:coluna**).
- Compatível com gramática em PT-BR (se habilitado em `keywords.py`):
  - `DECLARACOES, ALGORITMO, LER, IMPRIMIR, SE, ENTAO, SENAO, ENQUANTO, INICIO, FIM, E, OU, INTEIRO, REAL`.

---

## 🗂️ Estrutura do projeto

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
      parser.py      # (CP2)
      main.py
  tests/
    test_lexer_basic.py
```

---

## 🚀 Como executar

> Rode a partir da pasta **src**.

### Windows (PowerShell/CMD)
```powershell
cd src

# Análise léxica (lista tokens)
python -m minicompiler.main ..\examples\arquivo.mc
python -m minicompiler.main --lex ..\examples\arquivo.mc

# Análise sintática (parser)
python -m minicompiler.main --parse ..\examples\arquivo.mc
```

### Linux/macOS
```bash
cd src

# Léxico
python -m minicompiler.main ../examples/arquivo.mc
python -m minicompiler.main --lex ../examples/arquivo.mc

# Sintaxe
python -m minicompiler.main --parse ../examples/arquivo.mc
```

### Referência da CLI
```
python -m minicompiler.main [--lex | --parse] <caminho_do_arquivo.mc>

--lex   : roda só a análise léxica (DEFAULT)
--parse : roda a análise sintática (requer parser.py)
```

---

## 📝 Exemplo mínimo

`examples/sample.mc`
```txt
:DECLARACOES
x:INTEIRO

:ALGORITMO
x = 1
IMPRIMIR(x)
```

**Léxico — saída esperada**
```
COLON ':' @ 1:1
DECLARACOES 'DECLARACOES' @ 1:2
IDENTIFIER 'x' @ 2:1
COLON ':' @ 2:2
INTEIRO_TIPO 'INTEIRO' @ 2:3
COLON ':' @ 4:1
ALGORITMO 'ALGORITMO' @ 4:2
IDENTIFIER 'x' @ 5:1
ASSIGN '=' @ 5:3
INT_LIT '1' @ 5:5
IMPRIMIR 'IMPRIMIR' @ 6:1
LPAREN '(' @ 6:9
IDENTIFIER 'x' @ 6:10
RPAREN ')' @ 6:11
EOF '' @ 6:12
```

**Sintaxe — saída esperada**
```
OK: sintaxe válida.
```

## 🔧 Dicas e solução de problemas

- **“file not found”** → confira o caminho e rode a partir de `src/`.  
- **Caracteres estranhos no Windows** → use PowerShell em UTF-8.  
- **Erro léxico** (ex.: `invalid character '§'`) → remova o caractere inválido.  
- **Erro “Esperava fim do arquivo. Encontrado EOF”** → ajuste `_check` no parser para **não bloquear EOF**:
  ```python
  def _check(self, *types): return self._peek().type in types
  ```
- **Variável não declarada (ex.: `numero4`)** → **semântico** (fase seguinte), não léxico/sintaxe.

---

## ✅ Habilitando a gramática PT-BR (CP2)

No `keywords.py`, inclua:
```python
KEYWORDS.update({
  "DECLARACOES": TokenType.DECLARACOES,
  "ALGORITMO": TokenType.ALGORITMO,
  "LER": TokenType.LER,
  "IMPRIMIR": TokenType.IMPRIMIR,
  "SE": TokenType.SE,
  "ENTAO": TokenType.ENTAO,
  "SENAO": TokenType.SENAO,
  "ENQUANTO": TokenType.ENQUANTO,
  "INICIO": TokenType.INICIO,
  "FIM": TokenType.FIM,
  "E": TokenType.E,
  "OU": TokenType.OU,
  "INTEIRO": TokenType.INTEIRO_TIPO,
  "REAL": TokenType.REAL_TIPO,
})
```
No `lexer.py`, garanta:
- `":"` em `single_char` → `TokenType.COLON`
- números `INT_LIT` / `FLOAT_LIT`
- (opcional) strings para `IMPRIMIR("texto")`

---
