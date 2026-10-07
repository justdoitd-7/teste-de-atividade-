# 🕵️ Detector IA — Grupo 2

Projeto escolar em **Python + Streamlit** criado para ajudar pessoas a perceber possíveis indícios de conteúdo manipulado por inteligência artificial.

## O que o projeto faz

O sistema possui quatro áreas:

- 📝 Texto — analisa alguns padrões de escrita.
- 🖼️ Imagem — verifica características básicas da imagem.
- 🎥 Vídeo — verifica informações básicas do arquivo.
- 🔊 Áudio — verifica informações básicas do arquivo.

## ⚠️ Importante

Este é um **protótipo educativo**, não um detector profissional de IA.

Um detector real de deepfakes e conteúdo sintético precisa de modelos especializados, bancos de dados de treinamento e técnicas de análise forense. Portanto, o percentual mostrado pelo projeto representa apenas um **nível de suspeita baseado nos critérios implementados**.

## Como executar

### 1. Instale o Python

Recomenda-se Python 3.11 ou superior.

### 2. Abra o terminal na pasta do projeto

No VS Code, abra a pasta `detector_ia`.

### 3. Instale as bibliotecas

```bash
pip install -r requirements.txt
```

### 4. Execute o site

```bash
streamlit run codigo.py
```

O Streamlit deverá abrir o projeto no navegador.

## Estrutura

```text
detector_ia/
├── codigo.py
├── requirements.txt
└── README.md
```

## Ideia para apresentação

**Problema:** imagens, vídeos, áudios e textos podem ser manipulados por IA e muitas pessoas têm dificuldade para perceber.

**Solução:** criar uma ferramenta simples que analisa alguns sinais e apresenta um nível de suspeita.

**Público-alvo:** estudantes e usuários de redes sociais.

**Mensagem principal:** o sistema não substitui a verificação humana; ele funciona como um alerta.

## Melhorias futuras

- Usar modelos de visão computacional.
- Analisar metadados EXIF.
- Extrair quadros de vídeos.
- Detectar alterações em rostos.
- Analisar espectrogramas de áudio.
- Usar modelos especializados de detecção de conteúdo sintético.
