import pandas as pd
import numpy as np
import os

np.random.seed(42)

# =====================================================
# CONFIGURACAO GERAL
# =====================================================
caminho = r"C:\Users\juran\OneDrive\Área de Trabalho\Danielle Moreno - Case Maria Filo"
os.makedirs(caminho, exist_ok=True)

datas = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")

# =====================================================
# FUNCOES AUXILIARES
# =====================================================
def fator_sazonal_mes(mes):
    mapa = {
        1: 1.08, 2: 1.03, 3: 0.96, 4: 0.93,
        5: 0.95, 6: 0.98, 7: 1.00, 8: 1.03,
        9: 1.06, 10: 1.10, 11: 1.24, 12: 1.30
    }
    return mapa.get(mes, 1.0)

def fator_dia_semana(dia_semana):
    mapa = {
        0: 0.85,
        1: 0.90,
        2: 0.95,
        3: 1.00,
        4: 1.10,
        5: 1.20,
        6: 1.15
    }
    return mapa.get(dia_semana, 1.0)

def fator_data_comercial(data):
    mapa = {
        "03-08": 1.10,
        "03-15": 1.30,
        "06-12": 1.20,
        "09-15": 1.18,
        "10-12": 1.18,
        "11-11": 1.20,
        "11-27": 1.55,
        "11-30": 1.35,
    }

    mm_dd = data.strftime("%m-%d")
    fator = mapa.get(mm_dd, 1.0)

    if data.month == 1 and 5 <= data.day <= 31:
        fator *= 1.08

    if data.month == 2 and 1 <= data.day <= 20:
        fator *= 1.06

    if data.month == 3 and 20 <= data.day <= 31:
        fator *= 1.08
    if data.month == 4 and 1 <= data.day <= 10:
        fator *= 1.08

    if data.month == 5 and 1 <= data.day <= 12:
        fator *= 1.22

    if data.month == 6 and 1 <= data.day <= 12:
        fator *= 1.12

    if data.month == 8 and 1 <= data.day <= 12:
        fator *= 1.00

    if data.month == 9 and 8 <= data.day <= 15:
        fator *= 1.10

    if data.month == 10 and 5 <= data.day <= 12:
        fator *= 1.10

    if data.month == 11 and 1 <= data.day <= 30:
        fator *= 1.12

    if data.month == 12 and 1 <= data.day <= 24:
        fator *= 1.18

    return fator

def fator_colecao(colecao, mes):
    if colecao == "Verao" and mes in [1, 2, 11, 12]:
        return 1.10
    if colecao == "Outono" and mes in [3, 4, 5]:
        return 1.06
    if colecao == "Inverno" and mes in [6, 7, 8]:
        return 1.10
    if colecao == "Primavera" and mes in [9, 10]:
        return 1.06
    return 0.95

def gerar_custo_unitario(linha, preco_base):
    # Mantem a base original, mas deixa alfaiataria mais cara de produzir
    if linha == "Alfaiataria":
        fator = np.random.uniform(0.42, 0.58)
    elif linha == "Linho":
        fator = np.random.uniform(0.30, 0.45)
    elif linha in ["Jeans", "Tricot"]:
        fator = np.random.uniform(0.28, 0.40)
    else:
        fator = np.random.uniform(0.22, 0.35)
    return round(preco_base * fator, 2)

def fator_estrategia_ads(data):
    ano = data.year
    sazonal_mes = fator_sazonal_mes(data.month)
    sazonal_dia = fator_dia_semana(data.weekday())

    if ano == 2024:
        sazonal_data = 0.82

        if data.day <= 5 or data.day >= 25:
            sazonal_data *= 0.80

        sazonal_dia *= 0.92

    else:
        sazonal_data = fator_data_comercial(data)

        if data.day <= 5:
            sazonal_data *= 1.05

        if data.day >= 25:
            sazonal_data *= 1.04

    return sazonal_mes, sazonal_dia, sazonal_data, sazonal_mes * sazonal_dia * sazonal_data

def gerar_estoque_inicial(perfil, linha, ano_colecao, preco_base):
    if perfil == "Hero":
        return np.random.randint(70, 160)

    elif perfil == "Normal":
        if ano_colecao == 2024:
            return np.random.randint(120, 220)
        return np.random.randint(100, 180)

    else:
        # Encalhado: alfaiataria antiga e cara fica com estoque bem alto
        if linha == "Alfaiataria" and ano_colecao == 2024 and preco_base >= 300:
            return np.random.randint(240, 420)
        return np.random.randint(180, 320)

nomes_meses = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
}

nomes_dias = {
    0: "Segunda", 1: "Terca", 2: "Quarta", 3: "Quinta",
    4: "Sexta", 5: "Sabado", 6: "Domingo"
}

# =====================================================
# DIM_CALENDARIO
# =====================================================
dim_calendario = pd.DataFrame({
    "Data": datas,
    "Ano": datas.year,
    "Mes": datas.month,
    "Ano_Mes": datas.strftime("%Y-%m"),
    "Trimestre": "T" + datas.quarter.astype(str),
    "Semana_Ano": datas.isocalendar().week.astype(int),
    "Dia": datas.day,
    "Dia_Semana": datas.dayofweek
})

dim_calendario["Nome_Mes"] = dim_calendario["Mes"].map(nomes_meses)
dim_calendario["Nome_Dia"] = dim_calendario["Dia_Semana"].map(nomes_dias)
dim_calendario["Flag_Fim_Semana"] = np.where(dim_calendario["Dia_Semana"] >= 5, 1, 0)
dim_calendario["Fator_Data_Comercial"] = dim_calendario["Data"].apply(fator_data_comercial)
dim_calendario["Flag_Evento_Comercial"] = np.where(dim_calendario["Fator_Data_Comercial"] > 1, 1, 0)

# =====================================================
# DIM_PRODUTOS
# =====================================================
linhas = ["GGT", "Jeans", "Tricot", "Linho", "Alfaiataria", "Malhas"]
looks = ["Lisos", "Estampados", "Bordados", "Conjuntos", "Lurex"]
categorias = [
    "Blusas", "Regatas", "Camisas", "Jaquetas e Casacos", "T-Shirt",
    "Calcas", "Saias", "Shorts e Bermudas", "Vestidos", "Macacoes"
]
grupos = ["Top", "Bottom", "Full Look"]
colecoes = ["Verao", "Outono", "Inverno", "Primavera"]

dim_produtos = pd.DataFrame({
    "Id_Produto": range(1, 61),
    "Nome_Produto": [f"Produto {i}" for i in range(1, 61)],
    "Linha": np.random.choice(
        linhas,
        60,
        p=[0.10, 0.14, 0.14, 0.10, 0.30, 0.22]
    ),
    "Categoria": np.random.choice(categorias, 60),
    "Grupo": np.random.choice(grupos, 60),
    "Look": np.random.choice(looks, 60),
    "Colecao": np.random.choice(colecoes, 60),
    "Ano_Colecao": np.random.choice([2024, 2025], 60, p=[0.72, 0.28]),
    "Preco_Base": np.round(np.random.uniform(120, 380, 60), 2)
})

# Ajuste controlado: alfaiataria mais cara sem matar a distribuição original
mask_alf = dim_produtos["Linha"] == "Alfaiataria"
dim_produtos.loc[mask_alf, "Preco_Base"] = np.round(
    dim_produtos.loc[mask_alf, "Preco_Base"] * np.random.uniform(1.25, 1.55, mask_alf.sum()),
    2
)
dim_produtos["Preco_Base"] = dim_produtos["Preco_Base"].clip(upper=520)

dim_produtos["Colecao_Ano"] = dim_produtos["Colecao"] + " " + dim_produtos["Ano_Colecao"].astype(str)
dim_produtos["Flag_Colecao_Passada"] = np.where(dim_produtos["Ano_Colecao"] == 2024, 1, 0)

# Perfil do produto
dim_produtos["Perfil_Produto"] = "Normal"

# Hero = colecao 2025 + linhas comerciais + preco mais acessivel
cond_hero = (
    (dim_produtos["Ano_Colecao"] == 2025) &
    (dim_produtos["Linha"].isin(["Malhas", "Jeans", "Tricot"])) &
    (dim_produtos["Preco_Base"] <= dim_produtos["Preco_Base"].quantile(0.55))
)

# Encalhado = alfaiataria + colecao 2024 + preco mais alto
preco_corte_encalhado = dim_produtos.loc[
    dim_produtos["Linha"] == "Alfaiataria", "Preco_Base"
].quantile(0.55)

cond_encalhado = (
    (dim_produtos["Linha"] == "Alfaiataria") &
    (dim_produtos["Ano_Colecao"] == 2024) &
    (dim_produtos["Preco_Base"] >= preco_corte_encalhado)
)

dim_produtos.loc[cond_hero, "Perfil_Produto"] = "Hero"
dim_produtos.loc[cond_encalhado, "Perfil_Produto"] = "Encalhado"

# Garante alguns encalhados bem evidentes
candidatos_encalhados = dim_produtos[
    (dim_produtos["Linha"] == "Alfaiataria") &
    (dim_produtos["Ano_Colecao"] == 2024)
].copy()

if len(candidatos_encalhados) > 0:
    qtd_forcar = min(8, len(candidatos_encalhados))
    ids_forcar = candidatos_encalhados.nlargest(qtd_forcar, "Preco_Base").index
    dim_produtos.loc[ids_forcar, "Perfil_Produto"] = "Encalhado"

mapa_peso = {
    "Hero": 2.20,
    "Normal": 1.00,
    "Encalhado": 0.22
}
dim_produtos["Peso_Venda"] = dim_produtos["Perfil_Produto"].map(mapa_peso)

# =====================================================
# DIM_MARKETING
# =====================================================
dim_marketing = pd.DataFrame([
    {"Id_Marketing": 1, "Source": "google",    "Medium": "cpc",         "Canal_Midia": "Google Ads",     "Campaign": "Promo",         "Canal_Venda_Padrao": "Site"},
    {"Id_Marketing": 2, "Source": "google",    "Medium": "organic",     "Canal_Midia": "Google Organic", "Campaign": "SEO",           "Canal_Venda_Padrao": "Site"},
    {"Id_Marketing": 3, "Source": "instagram", "Medium": "paid_social", "Canal_Midia": "Instagram Ads",  "Campaign": "Remarketing",   "Canal_Venda_Padrao": "App"},
    {"Id_Marketing": 4, "Source": "facebook",  "Medium": "paid_social", "Canal_Midia": "Facebook Ads",   "Campaign": "Institucional", "Canal_Venda_Padrao": "Site"},
    {"Id_Marketing": 5, "Source": "direct",    "Medium": "none",        "Canal_Midia": "Direct",         "Campaign": "Direto",        "Canal_Venda_Padrao": "Site"},
    {"Id_Marketing": 6, "Source": "email",     "Medium": "email",       "Canal_Midia": "Email",          "Campaign": "CRM",           "Canal_Venda_Padrao": "Site"},
    {"Id_Marketing": 7, "Source": "referral",  "Medium": "referral",    "Canal_Midia": "Referral",       "Campaign": "Parceiros",     "Canal_Venda_Padrao": "Site"}
])

# =====================================================
# FATO_ESTOQUE
# =====================================================
fato_estoque = dim_produtos[["Id_Produto", "Linha", "Preco_Base", "Perfil_Produto", "Ano_Colecao"]].copy()

fato_estoque["Estoque_Atual"] = fato_estoque.apply(
    lambda row: gerar_estoque_inicial(
        row["Perfil_Produto"],
        row["Linha"],
        row["Ano_Colecao"],
        row["Preco_Base"]
    ),
    axis=1
)

fato_estoque["Custo_Unitario"] = fato_estoque.apply(
    lambda row: gerar_custo_unitario(row["Linha"], row["Preco_Base"]),
    axis=1
)

fato_estoque = fato_estoque[["Id_Produto", "Estoque_Atual", "Custo_Unitario"]]

# =====================================================
# FATO_ADS
# =====================================================
ads_lista = []
ids_midia_paga = [1, 3, 4]

for data in datas:
    ano = data.year
    sazonal_mes, sazonal_dia, sazonal_data, sazonal = fator_estrategia_ads(data)

    for id_marketing in ids_midia_paga:
        base_imp = {
            1: 16000,
            3: 14000,
            4: 11000
        }[id_marketing]

        base_ctr = {
            1: 0.028,
            3: 0.021,
            4: 0.017
        }[id_marketing]

        base_cpc = {
            1: 2.80,
            3: 1.85,
            4: 1.45
        }[id_marketing]

        impressoes = int(np.random.normal(base_imp * sazonal, base_imp * 0.10))
        impressoes = max(2500 if ano == 2024 else 4000, impressoes)

        ctr_real = np.random.uniform(base_ctr * 0.85, base_ctr * 1.15)

        if ano == 2024:
            ctr_real *= np.random.uniform(0.82, 0.94)
        else:
            ctr_real *= np.random.uniform(1.05, 1.15)
            if sazonal_data > 1.10:
                ctr_real *= np.random.uniform(1.02, 1.08)

        cliques = max(1, int(impressoes * ctr_real))

        cpc_real = np.random.uniform(base_cpc * 0.85, base_cpc * 1.05)

        if ano == 2024:
            cpc_real *= np.random.uniform(0.98, 1.08)
        else:
            if sazonal_data > 1.10:
                cpc_real *= np.random.uniform(1.08, 1.25)
            if sazonal_data > 1.30:
                cpc_real *= np.random.uniform(1.12, 1.32)

        custo = round(cliques * cpc_real, 2)

        ads_lista.append({
            "Data": data,
            "Id_Marketing": id_marketing,
            "Impressoes": impressoes,
            "Cliques": cliques,
            "Custo": custo
        })

fato_ads = pd.DataFrame(ads_lista)
fato_ads["CTR"] = fato_ads["Cliques"] / fato_ads["Impressoes"]
fato_ads["CPC"] = fato_ads["Custo"] / fato_ads["Cliques"]

# =====================================================
# FATO_GA_SESSIONS
# =====================================================
ga_lista = []

bases_sessoes = {
    1: 850,
    2: 650,
    3: 720,
    4: 520,
    5: 420,
    6: 180,
    7: 140
}

bases_conversao = {
    1: 0.0135,
    2: 0.0190,
    3: 0.0115,
    4: 0.0095,
    5: 0.0260,
    6: 0.0320,
    7: 0.0160
}

for data in datas:
    ano = data.year
    sazonal_mes, sazonal_dia, sazonal_data, sazonal = fator_estrategia_ads(data)

    for _, mk in dim_marketing.iterrows():
        id_marketing = mk["Id_Marketing"]

        if ano == 2024:
            fator_trafego = np.random.uniform(0.88, 0.98)
        else:
            fator_trafego = np.random.uniform(1.03, 1.10)

        sessoes = int(
            np.random.normal(
                bases_sessoes[id_marketing] * sazonal * fator_trafego,
                bases_sessoes[id_marketing] * 0.12
            )
        )
        sessoes = max(40, sessoes)

        usuarios = int(sessoes * np.random.uniform(0.74, 0.92))

        taxa_conv = np.random.uniform(
            bases_conversao[id_marketing] * 0.85,
            bases_conversao[id_marketing] * 1.15
        )

        if ano == 2024:
            taxa_conv *= np.random.uniform(0.80, 0.94)
        else:
            taxa_conv *= np.random.uniform(1.06, 1.18)
            if sazonal_data > 1.10:
                taxa_conv *= np.random.uniform(1.02, 1.08)

        conversoes = int(sessoes * taxa_conv)

        ga_lista.append({
            "Data": data,
            "Id_Marketing": id_marketing,
            "Sessoes": sessoes,
            "Usuarios": usuarios,
            "Conversoes": conversoes
        })

fato_ga_sessions = pd.DataFrame(ga_lista)

# =====================================================
# FATO_VENDAS
# =====================================================
vendas_lista = []

pesos_produtos = dim_produtos["Peso_Venda"].values
pesos_produtos = pesos_produtos / pesos_produtos.sum()

dim_produtos_idx = dim_produtos.set_index("Id_Produto")

for data in datas:
    ano = data.year
    ga_dia = fato_ga_sessions[fato_ga_sessions["Data"] == data]
    _, _, sazonal_data, _ = fator_estrategia_ads(data)

    for _, linha_ga in ga_dia.iterrows():
        id_marketing = linha_ga["Id_Marketing"]
        conversoes = linha_ga["Conversoes"]

        fator_pedido = np.random.uniform(0.55, 0.75)

        if ano == 2024:
            fator_pedido *= np.random.uniform(0.82, 0.94)
        else:
            fator_pedido *= np.random.uniform(1.05, 1.15)
            if sazonal_data > 1.10:
                fator_pedido *= np.random.uniform(1.02, 1.08)

        pedidos = max(0, int(conversoes * fator_pedido))
        if pedidos == 0:
            continue

        ids_escolhidos = np.random.choice(
            dim_produtos["Id_Produto"],
            size=pedidos,
            replace=True,
            p=pesos_produtos
        )

        produtos_sorteados = dim_produtos_idx.loc[ids_escolhidos].reset_index()

        for _, prod in produtos_sorteados.iterrows():
            fator_prod = fator_colecao(prod["Colecao"], data.month)
            perfil_prod = prod["Perfil_Produto"]
            ano_colecao = prod["Ano_Colecao"]

            if perfil_prod == "Hero":
                base_qtd = 1.60 if ano == 2025 else 1.35
            elif perfil_prod == "Normal":
                base_qtd = 1.30 if ano == 2025 else 1.15
            else:
                base_qtd = 0.55 if ano == 2025 else 0.65

            # Em 2025, colecao passada perde relevancia
            if ano == 2025 and ano_colecao == 2024:
                base_qtd *= 0.42

            # Alfaiataria antiga e cara sofre mais
            if (
                ano == 2025 and
                prod["Linha"] == "Alfaiataria" and
                ano_colecao == 2024 and
                prod["Preco_Base"] >= 300
            ):
                base_qtd *= 0.28

            base_qtd = max(base_qtd, 0.08)
            quantidade = max(1, min(np.random.poisson(base_qtd), 3))

            preco_venda = prod["Preco_Base"] * np.random.uniform(0.95, 1.12) * fator_prod

            if ano == 2025 and sazonal_data > 1.20 and data.month in [3, 5, 6, 11, 12]:
                preco_venda *= np.random.uniform(0.95, 1.00)

            if ano == 2024:
                preco_venda *= np.random.uniform(0.98, 1.03)

            # Janeiro/2025 com markdown em colecao passada
            if ano == 2025 and ano_colecao == 2024:
                preco_venda *= np.random.uniform(0.80, 0.92)

            # Markdown ainda mais forte para alfaiataria antiga e cara
            if (
                ano == 2025 and
                prod["Linha"] == "Alfaiataria" and
                ano_colecao == 2024 and
                prod["Preco_Base"] >= 300
            ):
                preco_venda *= np.random.uniform(0.72, 0.85)

            preco_venda = round(min(max(preco_venda, 90), 420), 2)

            canal_venda = dim_marketing.loc[
                dim_marketing["Id_Marketing"] == id_marketing,
                "Canal_Venda_Padrao"
            ].iloc[0]

            vendas_lista.append({
                "Data": data,
                "Id_Produto": prod["Id_Produto"],
                "Id_Marketing": id_marketing,
                "Quantidade": int(quantidade),
                "Preco_Venda": preco_venda,
                "Canal_Venda": canal_venda
            })

fato_vendas = pd.DataFrame(vendas_lista)

# =====================================================
# RECEITA NO GA
# =====================================================
receita_por_data_marketing = (
    fato_vendas
    .assign(Receita=lambda df: df["Quantidade"] * df["Preco_Venda"])
    .groupby(["Data", "Id_Marketing"], as_index=False)["Receita"]
    .sum()
)

fato_ga_sessions = fato_ga_sessions.merge(
    receita_por_data_marketing,
    on=["Data", "Id_Marketing"],
    how="left"
)

fato_ga_sessions["Receita"] = fato_ga_sessions["Receita"].fillna(0)

# =====================================================
# VALIDACOES BASICAS
# =====================================================
assert dim_calendario["Data"].is_unique, "dim_calendario[Data] precisa ser unica"
assert dim_produtos["Id_Produto"].is_unique, "dim_produtos[Id_Produto] precisa ser unica"
assert dim_marketing["Id_Marketing"].is_unique, "dim_marketing[Id_Marketing] precisa ser unica"

# =====================================================
# EXPORTACAO
# =====================================================
dim_calendario.to_csv(os.path.join(caminho, "dim_calendario.csv"), index=False, decimal=".")
dim_produtos.to_csv(os.path.join(caminho, "dim_produtos.csv"), index=False, decimal=".")
dim_marketing.to_csv(os.path.join(caminho, "dim_marketing.csv"), index=False, decimal=".")

fato_estoque.to_csv(os.path.join(caminho, "fato_estoque.csv"), index=False, decimal=".")
fato_ads.to_csv(os.path.join(caminho, "fato_ads.csv"), index=False, decimal=".")
fato_ga_sessions.to_csv(os.path.join(caminho, "fato_ga_sessions.csv"), index=False, decimal=".")
fato_vendas.to_csv(os.path.join(caminho, "fato_vendas.csv"), index=False, decimal=".")

print("Base gerada com sucesso.")
print(f"Arquivos salvos em: {caminho}")
print("Periodo: 2024 a 2025")
print("2024: estrategia de ads ineficiente e mal distribuida")
print("2025: estrategia aderente a datas comerciais e mais eficiente")
print("Produtos encalhados priorizados em: Alfaiataria + Colecao 2024 + Preco alto")
print("Campanhas mantidas sem alteracao estrutural")
print("Modelo pronto para Power BI em estrutura estrela e relacionamento 1:*")
