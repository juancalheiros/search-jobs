# Search Jobs

Este é um projeto Python para buscar vagas de emprego utilizando a API do RapidAPI.

## Funcionalidades

- Busca de vagas de emprego com base em palavras-chave.
- Suporte para filtros como país, tipo de trabalho (remoto ou presencial) e data de postagem.
- Salva os resultados em um arquivo JSON (`vagas.json`).

## Requisitos

- Python 3.14 ou superior
- Biblioteca `requests`
- Biblioteca `python-dotenv`

## Instalação

1. Clone este repositório ou faça o download do código.
2. Certifique-se de ter o Python instalado em sua máquina.
3. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie um arquivo `.env` na raiz do projeto e configure as seguintes variáveis de ambiente:
   ```
   URL_SEARCH_JOBS=https://jsearch.p.rapidapi.com/search
   API_KEY_RAPID=seu_api_key
   RAPID_API_HOST=jsearch.p.rapidapi.com
   QUERY_SEARCH=desenvolvedor fullstack
   NUM_PAGES=3
   COUNTRY=br
   DATA_POSTED=all
   REMOTE_JOB=false
   ```

## Uso

1. Execute o script principal:
   ```bash
   python main.py
   ```
2. O resultado será salvo no arquivo `vagas.json`.

3. O projeto pode ser rodado com o docker fazendo o build da imagem e rodando o container com esses comando no makefile
    ```bash
   make build
   ```
    ```bash
   make run
   ```

## Estrutura do Projeto

- `main.py`: Script principal para buscar vagas.
- `requirements.txt`: Lista de dependências do projeto.
- `README.md`: Documentação do projeto.
- `Makefile`: Comandos úteis para automação (opcional).
- `.env`: Arquivo para configuração de variáveis de ambiente.

## Exemplo de Saída

O arquivo `vagas.json` conterá uma lista de vagas no seguinte formato:

```json
[
    {
        "job_id": "12345",
        "job_title": "Desenvolvedor Fullstack",
        "company": "Empresa XYZ",
        "job_apply_link": "https://example.com/apply",
        "description": "Descrição da vaga...",
        "job_is_remote": true,
        "job_location": "São Paulo, SP",
        "job_google_link": "https://example.com",
        "apply_options": ["Opção 1", "Opção 2"]
    }
]
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

## Contato

- Autor: Juan de carvalho
- Email: [juancalheiros0001@gmail.com](mailto:juancalheiros0001@gmail.com)