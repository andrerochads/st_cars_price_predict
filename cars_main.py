# Imports
import pandas as pd
import numpy as np
import streamlit as st
import requests

# Read dataset
df = pd.read_csv('datasets/df3_processed.csv')


#--------------------------------------------------------------------------------------------------------------
# layout
#--------------------------------------------------------------------------------------------------------------

# Configurações gerais da página
st.set_page_config(layout="wide", page_title="Infinity Cars Tool", page_icon="icone.png")
st.markdown(
    """
    <style>
    /* Reduz o tamanho da caixa de seleção */
    select { 
        width: 150px;
        height: 30px;
        font-size: 12px;
    }
    /* Esconde a barra de rolagem vertical */
    body {
        overflow-y: hidden !important;
    }
    </style>
    """, 
    unsafe_allow_html=True)
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)

#--------------------------------------------------------------------------------------------------------------
# Functions
#--------------------------------------------------------------------------------------------------------------

# Limpar formulários
def clear_forms():
    selected_options = ['marca_s',
                        'modelo_s',
                        'tipo_s',
                        'combustivel_s',
                        'cambio_s',
                        'cilindradas_s',
                        'cor_s',
                        'blindado_s',
                        'hodometro_s',
                        'cidade_vendedor_s',
                        'ano_de_fabricacao_s',
                        'ano_modelo_s']
            
    for i in selected_options:
        st.session_state[i] = None



#--------------------------------------------------------------------------------------------------------------
# Conteúdo da Página
#--------------------------------------------------------------------------------------------------------------

# Título e Subtítulo do conteúdo
st.markdown('# Infinity Cars')
st.markdown('<p style="font-size:18px;">Preencha os campos abaixo com as características do veículo desejado. Vamos sugerir um preço para você.</p>', unsafe_allow_html=True)

# Colunas e seus conteúdos
col_main0, col_main1, col_main2, col_main3 = st.columns([2, 0.2, 3, 2.5])



#-----------
#----------------
#--------------------
# Coluna Principal 0 - Recebe caixas de seleção  
with col_main0:

    # Criando colunas para a caixas de seleção
    col1, col2 = st.columns(2)


    #-----------
    #----------------
    #------------------------------------------------------------------------------------------------------------------------------
    # Coluna com caixas de seleção de características 1 
    with col1:
        
        # Marca
        marca_options = df['marca'].drop_duplicates().to_list()
        marca_options.sort()
        selected_marca = st.selectbox("Marca", marca_options, index=None, key='marca_s')

        # Tipo
        tipo_options = df['tipo'].drop_duplicates().to_list()
        tipo_options.sort()
        selected_tipo = st.selectbox("Tipo", tipo_options, index=None, key='tipo_s')

        # Cambio
        cambio_options = df['cambio'].drop_duplicates().to_list()
        cambio_options.sort()
        selected_cambio = st.selectbox("Câmbio", cambio_options, index=None, key='cambio_s')

        # Cor
        cor_options = df['cor'].drop_duplicates().to_list()
        cor_options.sort()
        selected_cor = st.selectbox("Cor", cor_options, index=None, key='cor_s')

        # Hodometro
        selected_hodometro = st.text_input('Hodômetro (km)', placeholder='Write a km', key='hodometro_s')

        # Ano de fabricação
        ano_de_fabricacao_options = df['ano_de_fabricacao'].drop_duplicates().to_list()
        ano_de_fabricacao_options.sort(reverse=True)
        selected_ano_de_fabricacao = st.selectbox("Ano de Fabricação", ano_de_fabricacao_options, index=None, key='ano_de_fabricacao_s')

        # BOTÃO: Limpar campos (envia as informações para a API para realizar a predição)
        st.button('Limpar Campos', on_click=clear_forms)     


    #-----------
    #----------------
    #------------------------------------------------------------------------------------------------------------------------------
    # Coluna com caixas de seleção de características 2
    with col2:
        
        # Modelo
        if selected_marca:
            modelo_marca_options = df[df['marca'] == selected_marca][['modelo']].drop_duplicates()
            selected_modelo = st.selectbox("Modelo:", modelo_marca_options, index=None, key='modelo_s')
            
        else:
            modelo_marca_options = ['']
            selected_modelo = st.selectbox("Modelo:", modelo_marca_options, index=None, key='modelo_s')

        # Combustível
        combustivel_options = df['combustivel'].drop_duplicates().to_list()
        combustivel_options.sort()
        selected_combustivel = st.selectbox("Combustível", combustivel_options, index=None, key='combustivel_s')

        # Cilindradas
        cilindradas_options = df['cilindradas'].drop_duplicates().to_list()
        cilindradas_options.sort(reverse=True)
        selected_cilindradas = st.selectbox("Cilindradas", cilindradas_options, index=None, key='cilindradas_s')

        # Blindado
        blindado_options = df['blindado'].drop_duplicates().to_list()
        selected_blindado = st.selectbox("Blindado", blindado_options, index=None, key='blindado_s')

        # Cidade Vendedor
        cidade_vendedor_options = df['cidade_vendedor'].drop_duplicates().to_list()
        cidade_vendedor_options.sort()
        selected_cidade_vendedor = st.selectbox("Cidade", cidade_vendedor_options, index=None, key='cidade_vendedor_s')

        # Ano do Modelo
        if selected_ano_de_fabricacao:
            ano_modelo_options = [selected_ano_de_fabricacao, selected_ano_de_fabricacao + 1]
        else:
            ano_modelo_options = ['']  # Se não houver ano de fabricação selecionado
        selected_ano_modelo = st.selectbox("Ano Modelo:", ano_modelo_options, index=None, key='ano_modelo_s')

        # Criando Dict/json para a API
        # Obs.: essa ordem importa, quando se faz a solicitação para a API deve estar nessa ordem.
        data_to_api = {'marca': selected_marca,
                        'cor': selected_cor,
                        'combustivel': selected_combustivel,
                        'tipo': selected_tipo,
                        'cilindradas': selected_cilindradas,
                        'cidade_vendedor': selected_cidade_vendedor,
                        'ano_de_fabricacao': selected_ano_de_fabricacao,
                        'ano_modelo': selected_ano_modelo,
                        'hodometro': selected_hodometro,
                        'modelo': selected_modelo,
                        'cambio': selected_cambio,
                        'blindado': selected_blindado}

        # ---------------------------------------------------------------------------------------------------------------------
        # Comunicando com a API
        # ---------------------------------------------------------------------------------------------------------------------

        # O reciver False, mantém a estética sem valor predito e aguardado seleção...
        reciver = False
        
        # BOTÃO: Prever valor do veículo (envia as informações para a API para realizar a predição)
        lever_predict_button = False
        for chave, valor in data_to_api.items():
                if valor is None:
                    lever_predict_button = True

        if st.button('Sugerir valor', disabled=lever_predict_button):
            
            # Enviando dados para a API
            response = requests.post('https://api-cars-price-predict.onrender.com/api-cars-price-predict', json=data_to_api)

            # Retorno status_code
            if response.status_code == 200:
                
                # Transformando em json a resposta da API
                response_json = response.json()

                # Atribuindo apenas o valor da chave preco_sugerido à var de mesmo nome
                preco_sugerido = response_json[0].get('preco_sugerido')

                # Atribuindo valor predito para var valor_predito, para mostrar o valor para o usuário
                valor_predito = round(preco_sugerido, 2)

                # Apenas para melhorar a visualização, utilizado apenas para mostrar ao usuário
                valor_predito_formatado = '{:,.2f}'.format(valor_predito).replace(',', 'x').replace('.', ',').replace('x', '.')

                # Ativando o reciver para mostrar ao usuário outros conteúdos relacionados ao carro
                reciver = True

            else:
                st.write('Erro ao enviar dados para a API.')
                st.write(response.status_code)

        # Apenas para verificar os valores recebidos pelas keys session state    
        # st.write(st.session_state)
                

#-----------
#----------------
#------------------------------------------------------------------------------------------------------------------------------
with col_main1:
    st.write('') # Apenas para dar espaço (estético)

    # Filtro para fazer cálculos com os veículos semelhantes
    df_filtro_semelhantes = df[(df['marca'] == selected_marca) & 
                                (df['modelo'] == selected_modelo) & 
                                (df['ano_de_fabricacao'] == selected_ano_de_fabricacao)]



#-----------
#----------------
#------------------------------------------------------------------------------------------------------------------------------
# Coluna Principal 2 - Preço sugerido, check, estatísticas
with col_main2:  
    
    # Campo Preço Sugerido
    st.markdown("## Preço Sugerido:")

    if reciver:
        # Valor predito mostrado
        st.markdown(f'<h2 style="text-align: center; color: #4eed4e;">R$ {valor_predito_formatado}</h2>', unsafe_allow_html=True)

        # Mensagem de confirmação
        st.write(f'<p style="text-align: center; color: #4eed4e"> Valor predito com sucesso!</p>', unsafe_allow_html=True)

        # Valor médio dos semelhantes
        valor_medio_s = round(df_filtro_semelhantes['preco'].mean(), 2)
        # Desvio padrão dos semelhantes
        desvio_padrao_s = round(df_filtro_semelhantes['preco'].std(), 2)
        # Valor médio dos semelhantes - formatado
        valor_medio_s_formatado = '{:,.2f}'.format(valor_medio_s).replace(',', 'x').replace('.', ',').replace('x', '.')

        # Valor da médio para veículos semelhantes
        if np.isnan(valor_medio_s) == False:
            st.markdown(f'<p style="text-align: center;"> &#128202 Valor médio dos semelhantes: R$ {valor_medio_s_formatado} </p>', unsafe_allow_html=True)
     
        # Relação média e valor sugerido
        if valor_medio_s > valor_predito:

            # Abaixo da média
            diff_abaixo = round(valor_medio_s - valor_predito, 2)
            diff_abaixo_formatado = '{:,.2f}'.format(diff_abaixo).replace(',', 'x').replace('.', ',').replace('x', '.')
            st.markdown(f'<p style="text-align: center;"> &#x2B07 A sugestão está R$ {diff_abaixo_formatado} abaixo da média.</p>', unsafe_allow_html=True)

            # Confiabilidade da média
            if desvio_padrao_s <= valor_medio_s * 0.3:
                st.markdown(f'<p style="text-align: center;"> &#129001 Confiabilidade da média dos semelhantes: Alta! </p>', unsafe_allow_html=True)
            elif desvio_padrao_s >= valor_medio_s * 0.7:
                st.markdown(f'<p style="text-align: center;"> &#128997 Confiabilidade da média dos semelhantes: Baixa! </p>', unsafe_allow_html=True)
            else:
                st.markdown(f'<p style="text-align: center;"> &#129000 Confiabilidade da média dos semelhantes: Razoável! </p>', unsafe_allow_html=True)

        elif valor_medio_s < valor_predito:

            # Acima da média
            diff_acima = round(valor_predito - valor_medio_s, 2)
            diff_acima_formatado = '{:,.2f}'.format(diff_acima).replace(',', 'x').replace('.', ',').replace('x', '.')
            st.markdown(f'<p style="text-align: center;"> &#x2B06 A sugestão está R$ {diff_acima_formatado} acima da média.</p>', unsafe_allow_html=True)

            # Confiabilidade da média
            if desvio_padrao_s <= valor_medio_s * 0.3:
                st.markdown(f'<p style="text-align: center;"> &#129001 Confiabilidade da média dos semelhantes: Alta! </p>', unsafe_allow_html=True)
            elif desvio_padrao_s >= valor_medio_s * 0.7:
                st.markdown(f'<p style="text-align: center;"> &#128997 Confiabilidade da média dos semelhantes: Baixa! </p>', unsafe_allow_html=True)
            else:
                st.markdown(f'<p style="text-align: center;"> &#129000 Confiabilidade da média dos semelhantes: Razoável! </p>', unsafe_allow_html=True)

        else:
            st.write(f':sweat_smile: Porém, não existem veículos semelhantes em nossa base de dados.')
            st.write(f'Verifique se as características selecionadas para o veículo são possíveis.')     


        # Estatísticas Simples cálculos        
        st.write('') # Apenas para dar espaço
        st.write('') # Apenas para dar espaço

        # Total de semelhantes vendidos
        total_semelhantes = df_filtro_semelhantes['id'].count()

        # Estado mais vendido
        df_estado_mais_vendido = (df_filtro_semelhantes.loc[:, ['estado_vendedor', 'id']].groupby('estado_vendedor')
                                                                                        .count()
                                                                                        .sort_values('id', ascending=False)
                                                                                        .reset_index())
        estado_mais_vendido = df_estado_mais_vendido.iloc[0,0]
        estado_mais_vendido_qnt = df_estado_mais_vendido.iloc[0,1]

        # Cor predominante
        df_cor_predominante = (df_filtro_semelhantes.loc[:, ['cor', 'id']].groupby('cor')
                                                                .count()
                                                                .sort_values('id', ascending=False)
                                                                .reset_index())
        cor_predominante = df_cor_predominante.iloc[0,0]
        cor_predominante_qnt = df_estado_mais_vendido.iloc[0,1]

        # Marca x % base de dados
        filtro_marca = df[(df['marca'] == selected_marca)]
        total_marca_s = filtro_marca['marca'].count()
        total_marcas = df.shape[0]
        fatia_marca_s = round((total_marca_s / total_marcas)*100, 2)
        
        # Simples Estatísticas
        veiculo_marca_modelo = selected_marca + ' ' + selected_modelo
        st.markdown(f"##### Sobre semelhantes ao: {veiculo_marca_modelo} {selected_ano_de_fabricacao}")
        st.write(f'• Total de semelhantes vendidos: {total_semelhantes}')
        st.write(f'• Mais vendido no estado: ({estado_mais_vendido}) com {estado_mais_vendido_qnt} vendidos.')
        st.write(f'• Cor predominante: {cor_predominante} ({cor_predominante_qnt})')
        st.write(f'• Veículos {selected_marca} representam {fatia_marca_s}% da base de dados.')

    else:

        # Valor sugerido zerado ainda...
        st.markdown(f'<h2 style="text-align: center;">R$ --</h2>', unsafe_allow_html=True)

        # Mensagem aguardando seleção do veículo
        st.write(f'<h3 style="text-align: center; color: orange"> Aguardando seleção do veículo...</h3>', unsafe_allow_html=True)



#-----------
#----------------
#------------------------------------------------------------------------------------------------------------------------------
# Coluna Principal 3 - Tabela comparativa 
with col_main3:
    
    # Tabela preço, estado e regiao
    if reciver:

        st.markdown(f'#### Explore veículos semelhantes :oncoming_automobile:')

        # Tabela visão geral, preços no mercado
        df_tabela_semelhantes = (df_filtro_semelhantes[['preco',
                                                        'hodometro',
                                                        'modelo',
                                                        'ano_de_fabricacao', 
                                                        'ano_modelo',
                                                        'cor',
                                                        'tipo',
                                                        'combustivel',
                                                        'cilindradas',
                                                        'cambio',
                                                        'turbo', 
                                                        'offroad',
                                                        'blindado',
                                                        'marca',
                                                        'regiao',
                                                        'estado_vendedor', 
                                                        'cidade_vendedor',
                                                        'tipo_vendedor',
                                                        'veiculo_unico_dono',
                                                        'revisoes_concessionaria',
                                                        'garantia_de_fabrica',
                                                        'revisoes_dentro_agenda']])
        df_tabela_semelhantes['preco'] = df_tabela_semelhantes['preco'].apply(lambda x: round(x, 2))
        st.dataframe(df_tabela_semelhantes, height=480)

    else:
        imagem_local = 'images/car_ai.jpg'
        st.image(imagem_local, use_column_width=True, width=10)
        st.markdown(f"""<style>img {{border-radius: 15px;}}</style>""", unsafe_allow_html=True)
