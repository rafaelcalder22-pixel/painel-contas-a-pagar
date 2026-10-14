# Painel de Contas a Pagar

Site estático (HTML puro) com duas abas:

- **📊 Painel**: vencidas e a vencer por Regional, Praça, Empreendimento, Cargo e faixa de dias.
- **🖨️ Seleção para pagamento**: os mesmos filtros, caixas de seleção por conta e botão **Gerar extrato**, que abre a impressão (A4 paisagem) com: Empreendimento, Empresa, Obra, Proc., Confirmado, Cheque nominal, Vencimento, Prorrogação, Valor a pagar e Valor doc. fiscal, com subtotal por empreendimento e total geral.

Os dados ficam **criptografados** (AES-256 + PBKDF2) dentro do `index.html`. Sem a senha, nada é exibido.

## Publicar no GitHub Pages (grátis)

1. Crie um repositório **público** no GitHub (no plano gratuito, o Pages só funciona com repositório público).
2. Envie estes arquivos: `index.html`, `template.html`, `build.py`, `requirements.txt`, `README.md`, `.gitignore` e `.nojekyll`.
3. Em **Settings → Pages**, escolha **Deploy from a branch**, branch `main`, pasta `/ (root)` e salve.
4. O endereço será `https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/`.

## Atualizar com uma planilha nova

```bash
pip install -r requirements.txt
python build.py A_pagar_comissoes.xlsx      # lê só a aba "Detalhado"
```

A senha é pedida no terminal (ou use a variável `SENHA`). Depois, envie o `index.html` novo para o GitHub (commit e push, ou pelo botão *Upload files*).

A aba **Detalhado** precisa ter as colunas: Praça, Regional, Empreendimento, Dias a Vencer, Hoje, Cheque nominal, Vencimento, Prorrogação, Valor a pagar, Valor doc. fiscal, Cargo, Empresa, Obra, Proc., Confirmado.

## Segurança

- Como o repositório é público, o `index.html` também é. A proteção vem da criptografia: use uma senha **longa** (12+ caracteres) e que não use em outro lugar.
- **Nunca** envie a planilha (`.xlsx`) nem a senha ao GitHub (o `.gitignore` já bloqueia `.xlsx`).
- Quem souber a senha vê todos os dados. Se a senha vazar, gere um novo `index.html` com outra senha.
