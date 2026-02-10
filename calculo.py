# calculo.py
# By MGuimaraesN
from decimal import Decimal, ROUND_HALF_UP

IMPOSTO_PECA = Decimal("0.06")
IMPOSTO_SERVICO = Decimal("0.08")

TAXAS = {
    "visa": {
        "debito": Decimal("0.011"),
        "credito": {i: Decimal(str(v)) for i, v in {
            1: 0.0359, 2: 0.0486, 3: 0.0575, 4: 0.0664,
            5: 0.0752, 6: 0.0839, 7: 0.0960, 8: 0.1045,
            9: 0.1128, 10: 0.1210, 11: 0.1292, 12: 0.1372,
            13: 0.1506, 14: 0.1584, 15: 0.1662, 16: 0.1739,
            17: 0.1814, 18: 0.1889
        }.items()}
    },
    "elo": {
        "debito": Decimal("0.016"),
        "credito": {i: Decimal(str(v)) for i, v in {
            1: 0.0392, 2: 0.0597, 3: 0.0686, 4: 0.0775,
            5: 0.0863, 6: 0.0950, 7: 0.1065, 8: 0.1150,
            9: 0.1233, 10: 0.1315, 11: 0.1397, 12: 0.1477,
            13: 0.1606, 14: 0.1684, 15: 0.1762, 16: 0.1839,
            17: 0.1914, 18: 0.1989
        }.items()}
    }
}

def _q(v: Decimal) -> Decimal:
    return v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def parse_money(v) -> Decimal:
    if isinstance(v, (int, float)):
        return Decimal(str(v))
    s = str(v).strip().replace(".", "").replace(",", ".")  # aceita "1.234,56"
    return Decimal(s)

def calcular(peca, servico, forma, bandeira="elo", parcelas=1):
    peca = parse_money(peca)
    servico = parse_money(servico)

    if forma not in ("pix", "debito", "credito"):
        raise ValueError("forma inválida (use pix, debito, credito)")
    if bandeira not in TAXAS:
        raise ValueError("bandeira inválida")

    imposto_peca = peca * IMPOSTO_PECA
    imposto_servico = servico * IMPOSTO_SERVICO

    total_base = peca + servico

    taxa_maquina = Decimal("0")
    parcelas_out = None

    if forma == "debito":
        taxa_maquina = total_base * TAXAS[bandeira]["debito"]
    elif forma == "credito":
        if not (1 <= int(parcelas) <= 18):
            raise ValueError("parcelas inválidas (1..18)")
        parcelas_out = int(parcelas)
        taxa_maquina = total_base * TAXAS[bandeira]["credito"][parcelas_out]
    else:
        # pix: taxa 0 e sem parcelas
        pass

    acrescimo =  imposto_servico + taxa_maquina
    mao_obra_corrigida = servico + acrescimo
    total = peca + mao_obra_corrigida

    total = _q(total)
    mao_obra_corrigida = _q(mao_obra_corrigida)
    acrescimo = _q(acrescimo)

    valor_parcela = _q(total / parcelas_out) if parcelas_out else None

    return {
        "total": float(total),
        "mao_obra_corrigida": float(mao_obra_corrigida),
        "acrescimo": float(acrescimo),
        "imposto_peca": float(_q(imposto_peca)),
        "imposto_servico": float(_q(imposto_servico)),
        "taxa_maquina": float(_q(taxa_maquina)),
        "parcelas": parcelas_out,
        "valor_parcela": float(valor_parcela) if valor_parcela else None
    }