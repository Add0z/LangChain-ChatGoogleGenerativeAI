# LangChain Chat with Google Generative AI

Uma aplicação Streamlit que permite interação com inteligência artificial generativa usando LangChain e Google Gemini, com opções para busca baseada em PDFs carregados, Wikipedia e internet.

## Visão Geral

Este projeto implementa uma interface de chat inteligente com múltiplas fontes de informação:

- **Chat baseado em PDFs**: Carregue PDFs para gerar respostas baseadas em seu conteúdo (RAG - Retrieval Augmented Generation)
- **Chat baseado na Wikipedia**: Obtenha respostas baseadas em conhecimento da Wikipedia
- **Chat baseado na Internet**: Utilize o modelo Gemini para respostas baseadas no conhecimento geral

## Estrutura do Projeto

O projeto é estruturado com os seguintes componentes principais:

- `app.py`: Ponto de entrada principal da aplicação
- `Interface.py`: Gerencia a interface do usuário e a configuração do Streamlit
- `ChatApplication.py`: Controla a lógica principal do aplicativo de chat
- `ChatHistoryManager.py`: Gerencia o histórico de conversas
- `ChatRenderer.py`: Responsável pela renderização de mensagens com efeitos visuais
- `GeminiHelper.py`: Integração com a API do Google Generative AI (Gemini)
- `PdfVectorHelper.py`: Processamento de PDFs e criação de índices vetoriais
- `WikiHelper.py`: Busca e recuperação de informações da Wikipedia
- `InputCleaner.py`: Limpeza e processamento de entrada do usuário

## Requisitos

- Python 3.11
- Chave API do Google Generative AI

## Instalação

1. Clone o repositório:
```Terminal
git clone [URL_DO_REPOSITÓRIO]
cd [NOME_DO_DIRETÓRIO]
```

2. Instale as dependências:
```Terminal
pip install -r requirements.txt
```

3. Configure a chave API:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave API do Google Generative AI:
     ```
     GOOGLE_API_KEY=sua_chave_api_aqui
     ```

## Execução

Execute a aplicação Streamlit:

```Terminal
streamlit run app.py
```

O aplicativo será aberto em seu navegador padrão (geralmente http://localhost:8501).

## Uso

1. **Carregamento de PDFs**:
   - No menu lateral, clique em "Upload your PDF Files"
   - Selecione um ou mais PDFs
   - Clique em "Process" para indexar os documentos

2. **Escolha do modo de chat**:
   - Use os botões toggle para escolher entre:
     - 🛜 Use internet: Responde usando conhecimento geral da internet
     - 📃 Use PDFs: Responde baseado nos PDFs carregados
     - 🌐 Use Wikipedia(beta): Responde baseado em consultas à Wikipedia

3. **Interação com o Chat**:
   - Digite sua pergunta na caixa de texto
   - Pressione Enter para enviar
   - A resposta será exibida com um efeito de digitação

4. **Limpar o histórico**:
   - Clique em "Clear Chat History and Uploaded PDFs" para recomeçar

## Características Principais

- **Efeito de digitação**: Simulação de digitação em tempo real para resposta mais natural
- **Múltiplas fontes de conhecimento**: Flexibilidade para escolher entre PDFs, Wikipedia e internet
- **Processamento de PDFs**: Divisão de texto, geração de embeddings e busca por similaridade
- **Interface de usuário responsiva**: Layout clean e fácil navegação

## Tecnologias Utilizadas

- **Streamlit**: Interface de usuário web
- **LangChain**: Framework para aplicações de IA generativa
- **Google Generative AI (Gemini)**: Modelo de linguagem para geração de respostas
- **FAISS**: Biblioteca de busca por similaridade em vetores
- **PyPDF2**: Extração de texto de arquivos PDF
- **NLTK**: Processamento de linguagem natural
- **Wikipedia API**: Busca de informações na Wikipedia

## Solução de Problemas

- **Erro na API do Google**: Verifique se sua chave API está correta e se possui créditos suficientes
- **Problemas com PDFs**: Certifique-se que os PDFs estão em formato legível e não estão protegidos
- **Erros de NLTK**: Se ocorrerem erros relacionados ao NLTK, o sistema tentará usar uma versão simplificada

## Limitações

- O processamento de PDFs grandes pode levar algum tempo
- Algumas respostas da Wikipedia podem ser limitadas ou requerer buscas adicionais
- A qualidade das respostas depende da clareza da pergunta e da qualidade dos documentos carregados