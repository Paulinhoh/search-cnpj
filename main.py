import requests
import streamlit as st
import re


def format_cnpj(cnpj):
    if cnpj and len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj


def format_cep(cep):
    if cep and len(cep) == 8:
        return f"{cep[:5]}-{cep[5:]}"
    return cep


def format_cpf(cpf):
    if cpf and len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf


st.set_page_config(page_title="Busca CNPJ", layout="centered", page_icon="🏢")
st.title("Busca CNPJ da BrasilAPI 🏢")

st.markdown("Digite um CNPJ para buscar informações da empresa correspondente.")

cnpj_input = st.text_input(
    "CNPJ:", help="Aceita CNPJ com pontos, barras e traços ou apenas números."
)

if st.button("Buscar"):
    if cnpj_input:
        cnpj_clean = re.sub(r"\D", "", cnpj_input)
        if len(cnpj_clean) != 14:
            st.error("CNPJ inválido. Certifique-se de que possui 14 dígitos.")
        else:
            api_url = f"http://brasilapi.com.br/api/cnpj/v1/{cnpj_clean}"
            try:
                api_response = requests.get(api_url)
                if api_response.status_code == 200:
                    data = api_response.json()

                    st.success("Dados encontrados com sucesso!")

                    st.subheader("Informações da Empresa")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("📝 **Razão Social:**")
                        st.write(data.get("razao_social"))
                        st.write("🏷️ **Nome Fantasia:**")
                        st.write(data.get("nome_fantasia"))
                        st.write("🏢 **CNPJ:**")
                        st.write(format_cnpj(data.get("cnpj")))

                        st.write("💰 **Capital Social:**")
                        st.write(f"R$ {data.get('capital_social', 0):,.2f}")
                        st.write("📅 **Data de Abertura:**")
                        st.write(data.get("data_inicio_atividade"))
                        st.write("📞 **Telefones:**")
                        st.write(
                            f"{data.get('ddd_telefone_1')}, {data.get('ddd_telefone_2')}"
                        )

                    with col2:
                        st.write("📍 **Endereço:**")
                        st.write(
                            f"{data.get('descricao_tipo_de_logradouro')} {data.get('logradouro')}, {data.get('numero')}, {data.get('complemento')}"
                        )
                        st.write(
                            f"{data.get('bairro')}, {data.get('municipio')} - {data.get('uf')}"
                        )
                        st.write(f"**CEP:** {format_cep(data.get('cep'))}")
                        st.write("✉️ **E-mail:**")
                        st.write(data.get("email"))
                        st.write("💼 **Situação Cadastral:**")
                        st.write(data.get("descricao_situacao_cadastral"))
                        st.write("📅 **Data da Situação Cadastral:**")
                        st.write(data.get("data_situacao_cadastral"))
                        st.write("📜 **Regime de Tributação:**")

                        regimes = data.get("regime_tributario", [])
                        regime = regimes[-1] if regimes else None
                        st.write(regime.get("forma_de_tributacao") if regime else "N/A")

                    st.subheader("Socios:")
                    sucios = data.get("qsa", [])
                    if sucios:
                        for socio in sucios:
                            st.write(f"👤 **Nome:** {socio.get('nome_socio')}")
                            st.write(
                                f"📇 **CPF/CNPJ:** {format_cpf(socio.get('cnpj_cpf_do_socio'))}"
                            )
                            st.write(
                                f"📌 **Qualificação:** {socio.get('qualificacao_socio')}"
                            )
                            st.write(
                                f"📆 **Data de Entrada na sociedade:** {socio.get('data_entrada_socio')}"
                            )
                            st.write("---")
                    else:
                        st.write("Nenhum sócio encontrado.")

                    st.subheader("Atividades")
                    st.write("**Atividade Principal:**")
                    st.write(f"- {data.get('cnae_fiscal_descricao')}")

                    if data.get("cnaes_secundarios"):
                        st.write("**Atividades Secundárias:**")
                        for atividade in data.get("cnaes_secundarios", []):
                            st.write(f"- {atividade.get('descricao')}")

                else:
                    st.error("CNPJ não encontrado na base de dados.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao buscar o CNPJ: {e}")
    else:
        st.error("Por favor, insira um CNPJ para buscar.")
