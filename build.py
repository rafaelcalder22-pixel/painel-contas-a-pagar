#!/usr/bin/env python3
"""Gera o index.html (com os dados criptografados) a partir da planilha.

Uso:  python build.py A_pagar_comissoes.xlsx
A senha é lida da variável SENHA ou pedida no terminal (nunca fica salva no projeto).
"""
import sys, os, json, base64, getpass
import pandas as pd
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ABA = 'Detalhado'
ITER = 250_000
COLS = ['Praça', 'Regional', 'Empreendimento', 'Dias a Vencer', 'Hoje', 'Cheque nominal', 'Vencimento',
        'Prorrogação', 'Valor a pagar', 'Valor doc. fiscal', 'Cargo', 'Empresa', 'Obra', 'Proc.', 'Confirmado']

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    df = pd.read_excel(sys.argv[1], sheet_name=ABA)
    falt = [c for c in COLS if c not in df.columns]
    if falt:
        sys.exit(f'Colunas ausentes na aba {ABA}: {falt}')
    senha = os.environ.get('SENHA') or getpass.getpass('Senha de acesso ao painel: ')
    if len(senha) < 8:
        sys.exit('Use uma senha com pelo menos 8 caracteres (de preferência 12 ou mais).')

    df['Cargo'] = df['Cargo'].astype(str).str.strip()
    R, P, E, G = (sorted(df[c].unique()) for c in ['Regional', 'Praça', 'Empreendimento', 'Cargo'])
    iso = lambda v: v.strftime('%Y-%m-%d')
    rows = [[R.index(r['Regional']), P.index(r['Praça']), E.index(r['Empreendimento']), int(r['Dias a Vencer']),
             str(r['Cheque nominal']).strip(), iso(r['Vencimento']), round(float(r['Valor a pagar']), 2),
             round(float(r['Valor doc. fiscal']), 2), G.index(r['Cargo']), str(r['Empresa']), str(r['Obra']),
             str(r['Proc.']), '' if pd.isna(r['Confirmado']) else str(r['Confirmado']), iso(r['Prorrogação'])]
            for _, r in df.iterrows()]
    payload = json.dumps({'L': {'R': R, 'P': P, 'E': E, 'G': G}, 'rows': rows, 'hoje': iso(df['Hoje'].iloc[0])},
                         ensure_ascii=False, separators=(',', ':')).encode()

    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(senha.encode())
    ct = AESGCM(key).encrypt(iv, payload, None)
    b = lambda x: base64.b64encode(x).decode()
    enc = json.dumps({'s': b(salt), 'i': b(iv), 'c': b(ct), 'n': ITER})

    here = os.path.dirname(os.path.abspath(__file__))
    html = open(os.path.join(here, 'template.html'), encoding='utf8').read().replace('__ENC__', enc)
    open(os.path.join(here, 'index.html'), 'w', encoding='utf8').write(html)
    print(f'index.html gerado: {len(rows)} títulos, total R$ {df["Valor a pagar"].sum():,.2f}')

if __name__ == '__main__':
    main()
