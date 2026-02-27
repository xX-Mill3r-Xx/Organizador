# 📁 Organizador de Pastas em Python

**Organizador** é um projeto em **Python** que automatiza a organização de arquivos em pastas com base em seus tipos/extensões.
Ele foi criado para facilitar o gerenciamento de diretórios cheios de arquivos variados (como `imagens`, `documentos`, `vídeos`, etc.), movendo automaticamente cada arquivo para a pasta correta.

✨ Este projeto é ideal para automatizar a limpeza de pastas como **Downloads**, **Desktop** ou qualquer outra estrutura de arquivos desorganizada.

## 🧠 Funcionalidade

O script principal do projeto:

✔︎ Percorre todos os arquivos dentro de uma pasta selecionada
✔︎ Identifica o tipo/extensão de cada arquivo
✔︎ Cria subpastas automaticamente, se elas ainda não existirem
✔︎ Move os arquivos para as pastas correspondentes às suas extensões

Por exemplo:

* Arquivos `.jpg`, `.png`, `.gif` → movidos para a pasta `Imagens`
* Arquivos `.pdf`, `.docx` → movidos para a pasta `Documentos`
* Arquivos sem extensão ou tipos não previstos → movidos para uma pasta `Outros`

## 🚀 Começando

### 🔧 Pré-requisitos

Antes de tudo, certifique-se de ter:

* Python 3.x instalado em seu sistema
* Um terminal ou prompt de comando funcionando

### 📌 Instalação / Download

1. Clone o repositório:

   ```bash
   git clone https://github.com/xX-Mill3r-Xx/Organizador.git
   ```

2. Entre na pasta do projeto:

   ```bash
   cd Organizador/Organizador_Python
   ```

## ▶️ Como usar

1. Abra o terminal ou prompt de comando.

2. Execute o script principal do organizador:

   ```bash
   python main.py
   ```

3. Quando solicitado, **digite o caminho da pasta** que deseja organizar.

4. Aguarde enquanto os arquivos são organizados automaticamente.

📌 Se quiser testar com uma pasta de exemplo, você pode criar uma estrutura de arquivos com vários tipos (ex: `.jpg`, `.pdf`, `.mp4`, etc.) e rodar o script sobre ela.

## 💡 Ideias de melhorias

Este projeto já é funcional, mas você pode expandi-lo com:

* 📌 Organização por **data de criação** dos arquivos
* 🚀 Interface gráfica (GUI) com `tkinter` ou `PyQt`
* 📦 Suporte a arquivos dentro de subpastas
* 🧠 Detector de tipos mais avançado (usando mime types)
* 🛠️ Adição de testes automatizados

## 📄 Licença

O projeto usa a **MIT License** — isso significa que você pode reutilizá-lo e modificá-lo livremente, desde que mantenha os créditos originais no código.

