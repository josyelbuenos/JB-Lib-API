
# 📚 JB-LIB - Scraper de Livros ZLibrary

**📚 JB-LIB** é uma aplicação Flask desenvolvida para buscar informações sobre livros a partir do site ZLibrary. O scraper coleta dados básicos como título, autor, ano, idioma, editora e também detalhes adicionais como descrição, categoria e páginas de cada livro. Além disso, oferece a opção de ler o livro online diretamente pelo site.

## 📑Descrição do Projeto

Este projeto é uma API RESTful que utiliza Flask para fornecer endpoints que permitem buscar livros por meio de consultas, obter informações detalhadas de um livro específico e acessar links para leitura online.

A aplicação utiliza a biblioteca **BeautifulSoup** para parsear o HTML das páginas da ZLibrary e extrair as informações desejadas. Além disso, implementa o uso de cache com a função `lru_cache` para otimizar o acesso aos detalhes de cada livro.

## ✅Funcionalidades

- **Busca de livros**: Permite buscar livros com base em uma consulta, retornando até 12 livros por pesquisa.
- **Detalhes do livro**: Captura informações detalhadas sobre um livro específico, incluindo descrição, categoria, páginas e link para leitura online.
- **Cache de detalhes**: Utiliza cache para armazenar detalhes dos livros acessados recentemente e melhorar a performance.

## 🔍Endpoints da API

### 1. **GET `/busca`**

Realiza uma busca básica por livros.

#### Parâmetros:
- `query`: A consulta para buscar os livros (obrigatório).

#### Exemplo de resposta:
```json
[
  {
    "Título": "Nome do Livro",
    "Autor": "Autor do Livro",
    "Ano": "2024",
    "Idioma": "Português",
    "Editora": "Editora Exemplo",
    "URL": "https://z-library.sk/exemplo-livro"
  }
]
```

### 2. **GET `/livro`**

Captura detalhes de um livro específico a partir do link da página.

#### Parâmetros:
- `link`: URL do livro na ZLibrary (obrigatório).

#### Exemplo de resposta:
```json
{
  "Título Detalhado": "Nome do Livro",
  "Descrição": "Descrição do livro...",
  "Categoria": "Ficção",
  "Páginas": "200",
  "Leia Online": "https://z-library.sk/leitura-online"
}
```

## ⚙️Instalação

### 📃Requisitos
- Python 3.x
- pip

### ✍🏻Passos para execução

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/JB-LIB.git
   ```

2. Acesse a pasta do projeto:
   ```bash
   cd JB-LIB
   ```

3. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

5. Execute o servidor Flask:
   ```bash
   python app.py
   ```

6. Acesse a API na URL `http://127.0.0.1:5000/`.

## Links

- [Documentação Completa](https://document-jb-lib.vercel.app/)
  
## 🤝 Contribuições

Sinta-se à vontade para abrir *issues* e enviar *pull requests* para melhorias ou correções. Toda contribuição é bem-vinda!

## 🪪 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🎩 Autor

- [@josyelbuenos](https://www.github.com/josyelbuenos)

