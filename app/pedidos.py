"""Regras de pedido usadas na Aula 03 de DevOps.

O objetivo do arquivo nao e construir um e-commerce completo. O objetivo e
ter regras pequenas o suficiente para testar, refatorar e automatizar.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

CENTAVOS = Decimal("0.01")
CUPONS_VALIDOS: dict[str, Decimal] = {
    "DEVOPS10": Decimal("10"),
    "FAG15": Decimal("15"),
}
CUPOM_FRETE_EXPRESSO_GRATIS = "FRETEEXPRESSO"
LIMITE_FRETE_EXPRESSO_GRATIS = Decimal("50.00")


@dataclass(frozen=True)
class ItemPedido:
    nome: str
    preco_unitario: Decimal
    quantidade: int

    def subtotal(self) -> Decimal:
        if self.preco_unitario < 0:
            raise ValueError("preco_unitario nao pode ser negativo")
        if self.quantidade <= 0:
            raise ValueError("quantidade precisa ser maior que zero")
        return dinheiro(self.preco_unitario * self.quantidade)


@dataclass(frozen=True)
class Pedido:
    itens: list[ItemPedido]
    desconto_percentual: Decimal = Decimal("0")
    cupom: str | None = None
    entrega_expressa: bool = False


def dinheiro(valor: Decimal) -> Decimal:
    """Arredonda valores monetarios para duas casas decimais."""
    return valor.quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def validar_desconto(percentual: Decimal) -> None:
    if percentual < 0 or percentual > 100:
        raise ValueError("desconto_percentual precisa estar entre 0 e 100")


def calcular_subtotal(itens: list[ItemPedido]) -> Decimal:
    if not itens:
        raise ValueError("pedido precisa ter pelo menos um item")
    return dinheiro(sum((item.subtotal() for item in itens), Decimal("0")))


def aplicar_desconto_percentual(subtotal: Decimal, percentual: Decimal) -> Decimal:
    validar_desconto(percentual)
    desconto = subtotal * (percentual / Decimal("100"))
    return dinheiro(subtotal - desconto)


def percentual_do_cupom(cupom: str | None) -> Decimal:
    if cupom is None or cupom == "":
        return Decimal("0")
    cupom_normalizado = cupom.strip().upper()
    if cupom_normalizado in CUPONS_VALIDOS:
        return CUPONS_VALIDOS[cupom_normalizado]
    if cupom_normalizado == CUPOM_FRETE_EXPRESSO_GRATIS:
        return Decimal("0")
    raise ValueError("cupom invalido")


def cupom_libera_frete_expresso(cupom: str | None) -> bool:
    if cupom is None:
        return False
    return cupom.strip().upper() == CUPOM_FRETE_EXPRESSO_GRATIS


def calcular_frete(
    subtotal_com_desconto: Decimal,
    entrega_expressa: bool,
    frete_expresso_gratis: bool = False,
) -> Decimal:
    if subtotal_com_desconto >= Decimal("200") and not entrega_expressa:
        return Decimal("0.00")
    if entrega_expressa:
        if frete_expresso_gratis and subtotal_com_desconto > LIMITE_FRETE_EXPRESSO_GRATIS:
            return Decimal("0.00")
        return Decimal("29.90")
    return Decimal("14.90")


def calcular_total_pedido(pedido: Pedido) -> Decimal:
    subtotal = calcular_subtotal(pedido.itens)
    apos_desconto = aplicar_desconto_percentual(subtotal, pedido.desconto_percentual)
    cupom_percentual = percentual_do_cupom(pedido.cupom)
    apos_cupom = aplicar_desconto_percentual(apos_desconto, cupom_percentual)
    frete_expresso_gratis = cupom_libera_frete_expresso(pedido.cupom)
    frete = calcular_frete(apos_cupom, pedido.entrega_expressa, frete_expresso_gratis)
    return dinheiro(apos_cupom + frete)
