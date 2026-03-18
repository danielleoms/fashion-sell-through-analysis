# 📊 Sell-Through & Inventory Performance Analysis

## 📌 Visão Geral

Este projeto apresenta uma análise completa de desempenho de produtos no varejo, utilizando a métrica de **sell-through** como principal indicador para avaliar eficiência de vendas e identificar oportunidades de otimização de estoque.

O objetivo é apoiar decisões comerciais mais assertivas, como estratégias de precificação, campanhas e liquidação de produtos.

---


## 🖥️ Visualização do Dashboard

[Dashboard Sell-Through & Inventory Performance Analysis]([https://app.powerbi.com/view?r=eyJrIjoiNGYzZDU2NmUtZGYxYy00ZjczLWEzNWItNzA1OGY0ZWEyZTM4IiwidCI6IjZkYzZjNzEyLWZhYTYtNDgxZS1hMmE0LTdiOGI3ZWZjM2U3NSJ9](https://app.powerbi.com/view?r=eyJrIjoiNGYzZDU2NmUtZGYxYy00ZjczLWEzNWItNzA1OGY0ZWEyZTM4IiwidCI6IjZkYzZjNzEyLWZhYTYtNDgxZS1hMmE0LTdiOGI3ZWZjM2U3NSJ9&pageName=f625580d72775b31670d))


## 🧪 Engenharia de Dados (Simulação)

Os dados foram gerados utilizando **Python**, simulando um ambiente de **data lake real de varejo**.

A modelagem contempla:

* Histórico de vendas
* Níveis de estoque ao longo do tempo
* Atributos estratégicos de produto (linha, coleção, faixa de preço)

Essa abordagem permite trabalhar com cenários realistas e validar regras de negócio em um contexto próximo ao ambiente corporativo.

---

## 📈 Principais Indicadores

* **Sell-through (%)** → Eficiência de venda sobre o total disponível
* **Estoque Atual** → Volume disponível para comercialização
* **Classificação de Performance** → Segmentação de produtos por desempenho
* **Ações Sugeridas** → Direcionamento estratégico baseado em dados

---

## 🧠 Lógica de Negócio

### Sell-through

Sell-through = Vendido / (Vendido + Estoque atual)

### Classificação de Performance

* 🔴 **Encalhado** → ST < 30%
* 🟠 **Baixo Giro** → ST < 50%
* 🟡 **Performance Média** → ST entre 50% e 70%
* 🟢 **Alta Performance** → ST ≥ 70%

---

## ⚠️ Motor de Decisão (Ações Sugeridas)

As recomendações são geradas com base em múltiplas variáveis:

* Linha do produto
* Ano da coleção
* Posicionamento de preço
* Sell-through
* Nível de estoque

### Exemplos de decisões:

* Produtos com baixo desempenho e alto estoque → **Liquidação ou campanha**
* Produtos com performance intermediária → **Ajuste de preço**
* Produtos com alta performance → **Manutenção da estratégia atual**

---

## 🛠️ Stack Tecnológica

* **Power BI** → Visualização e construção do dashboard
* **DAX** → Modelagem de métricas e regras de negócio
* **Python** → Geração e simulação dos dados

---

## 📷 Dashboard

![Dashboard](imagens/dashboard.png)

---

## 💡 Principais Insights

* Identificação rápida de produtos com baixa performance
* Priorização de ações comerciais baseada em dados
* Apoio à gestão estratégica de estoque
* Visão integrada entre vendas e disponibilidade

---

## 👤 Autor

**Danielle Moreno**
Data Analyst | Business Intelligence
