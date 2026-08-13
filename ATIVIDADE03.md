# Atividade 03 — Testes automatizados e feedback local

Sistema de pedidos com ciclo local de qualidade: testes automatizados, cobertura e lint,
reunidos em um unico comando (`make quality`).

## O que foi feito

- Regras de negocio em `app/pedidos.py`: subtotal, desconto percentual, cupom, frete.
- CLI em `app/cli.py` para calcular o total de um pedido pelo terminal.
- Suite de testes em `tests/` (unitarios e de integracao da CLI).
- `pyproject.toml` configurando pytest, cobertura de branch e ruff.
- `Makefile` com os atalhos `install`, `test`, `cov`, `lint` e `quality`.

## Nova regra de negocio

Cupom `FRETEEXPRESSO`: nao concede desconto percentual, mas zera o valor do frete expresso
quando o total do pedido (ja com desconto) excede R$ 50,00. O campo `cupom` continua unico
(`str | None`), entao o sistema segue aceitando somente um cupom por pedido.

Implementado em `app/pedidos.py` (`cupom_libera_frete_expresso`, parametro novo em
`calcular_frete`) e coberto por testes em `tests/test_pedidos.py`.

## Resultado das verificacoes

```text
ruff check .          -> All checks passed!
pytest --cov=app      -> 33 passed, 96% cobertura
make quality          -> lint + testes + cobertura, sem erros
```
