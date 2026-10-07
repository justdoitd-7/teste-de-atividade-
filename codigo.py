import streamlit as st
from PIL import Image, ImageStat, ImageFilter
import io
import re
import math
import hashlib

st.set_page_config(
    page_title="Detector IA",
    page_icon="🕵️",
    layout="wide",
)

# ---------- ESTILO ----------
st.markdown("""
<style>
    .main-title {
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 18px;
        opacity: .8;
        margin-top: 0;
    }
    .result-box {
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,.25);
        margin-top: 15px;
    }
    .small-note {
        font-size: 13px;
        opacity: .7;
    }
</style>
""", unsafe_allow_html=True)

# ---------- FUNÇÕES DE ANÁLISE ----------

def calcular_nivel(pontos):
    pontos = max(0, min(100, int(round(pontos))))
    if pontos < 30:
        return "Baixa", "🟢", "Poucos indícios de manipulação."
    if pontos < 60:
        return "Média", "🟡", "Existem alguns indícios que merecem atenção."
    if pontos < 80:
        return "Alta", "🟠", "Foram encontrados vários indícios de manipulação."
    return "Muito alta", "🔴", "O conteúdo apresenta muitos indícios suspeitos."


def analisar_texto(texto):
    pontos = 0
    motivos = []

    if len(texto.strip()) < 40:
        pontos += 5
        motivos.append("O texto é muito curto para uma análise confiável.")

    palavras = re.findall(r"\b[\wÀ-ÿ'-]+\b", texto.lower())
    total = len(palavras)

    if total:
        frases = re.split(r"[.!?]+", texto)
        frases_validas = [f.strip() for f in frases if f.strip()]
        if frases_validas:
            tamanhos = [len(re.findall(r"\b[\wÀ-ÿ'-]+\b", f)) for f in frases_validas]
            media = sum(tamanhos) / len(tamanhos)
            variacao = (
                math.sqrt(sum((x - media) ** 2 for x in tamanhos) / len(tamanhos))
                if len(tamanhos) > 1 else 0
            )
            if media > 28 and variacao < 7:
                pontos += 20
                motivos.append("As frases possuem comprimento muito uniforme.")

    conectores = [
        "além disso", "nesse sentido", "dessa forma", "por outro lado",
        "portanto", "em suma", "é importante destacar", "vale ressaltar"
    ]
    encontrados = sum(1 for c in conectores if c in texto.lower())
    if encontrados >= 3:
        pontos += 15
        motivos.append("Há uso frequente de conectores formais e repetitivos.")

    if re.search(r"\b(100%|com certeza|sem dúvida|sempre|nunca)\b", texto.lower()):
        pontos += 10
        motivos.append("Há afirmações muito categóricas.")

    if total > 120 and texto.count("\n") == 0:
        pontos += 10
        motivos.append("O texto é extenso e possui pouca variação visual.")

    if not motivos:
        motivos.append("Nenhum padrão forte foi encontrado pelos critérios desta demonstração.")

    nivel, emoji, resumo = calcular_nivel(pontos)
    return pontos, nivel, emoji, resumo, motivos


def analisar_imagem(uploaded_file):
    dados = uploaded_file.getvalue()
    imagem = Image.open(io.BytesIO(dados)).convert("RGB")
    largura, altura = imagem.size

    pontos = 0
    motivos = []

    # Verificações simples e educativas. Não substituem um detector forense.
    if largura >= 1000 and altura >= 1000:
        pontos += 10
        motivos.append("A imagem possui alta resolução.")

    estatisticas = ImageStat.Stat(imagem)
    media = sum(estatisticas.mean) / 3
    if 35 < media < 220:
        pontos += 5
        motivos.append("A distribuição média de luminosidade foi considerada comum.")

    # Detecta excesso de regiões muito lisas/sem variação como um sinal fraco.
    pequena = imagem.resize((128, 128))
    bordas = pequena.filter(ImageFilter.FIND_EDGES)
    edge_stat = ImageStat.Stat(bordas)
    media_borda = sum(edge_stat.mean) / 3
    if media_borda < 8:
        pontos += 15
        motivos.append("Poucas bordas/variações foram encontradas; isso pode ocorrer em imagens muito suavizadas.")

    # Hash serve apenas para identificar o arquivo durante a sessão.
    hash_arquivo = hashlib.sha256(dados).hexdigest()[:12]

    if not motivos:
        motivos.append("Nenhum indício forte foi encontrado pelos critérios básicos.")

    nivel, emoji, resumo = calcular_nivel(pontos)
    return pontos, nivel, emoji, resumo, motivos, (largura, altura), hash_arquivo, imagem


def analisar_midia(uploaded_file):
    dados = uploaded_file.getvalue()
    tamanho_mb = len(dados) / (1024 * 1024)
    pontos = 0
    motivos = []

    if tamanho_mb < 0.05:
        pontos += 10
        motivos.append("O arquivo possui tamanho muito pequeno; isso limita a análise.")

    extensao = uploaded_file.name.lower().split(".")[-1]
    if extensao in {"mp4", "mov", "webm", "avi", "mp3", "wav", "ogg", "m4a"}:
        pontos += 5
        motivos.append("Formato de mídia reconhecido.")

    if not motivos:
        motivos.append("Nenhum indício forte foi encontrado pelos critérios básicos.")

    nivel, emoji, resumo = calcular_nivel(pontos)
    return pontos, nivel, emoji, resumo, motivos, tamanho_mb


# ---------- CABEÇALHO ----------
st.markdown('<p class="main-title">🕵️ Detector IA</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Uma ferramenta educativa para analisar indícios de conteúdo manipulado por inteligência artificial.</p>',
    unsafe_allow_html=True
)

st.info(
    "⚠️ Importante: este projeto é um protótipo escolar. Ele não consegue provar que um conteúdo foi criado por IA. "
    "O resultado representa apenas um nível de suspeita baseado em critérios simples."
)

# ---------- MENU ----------
tipo = st.sidebar.radio(
    "Escolha o tipo de conteúdo:",
    ["📝 Texto", "🖼️ Imagem", "🎥 Vídeo", "🔊 Áudio"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Projeto escolar — Grupo 2: IA e conteúdos manipulados")

# ---------- TEXTO ----------
if tipo == "📝 Texto":
    st.header("📝 Analisar texto")
    st.write("Cole um texto abaixo e veja alguns padrões que podem indicar geração automática.")

    texto = st.text_area(
        "Digite ou cole o texto:",
        height=240,
        placeholder="Cole aqui o conteúdo que deseja analisar..."
    )

    if st.button("🔎 Analisar texto", use_container_width=True):
        if not texto.strip():
            st.warning("Digite algum texto antes de analisar.")
        else:
            pontos, nivel, emoji, resumo, motivos = analisar_texto(texto)

            st.subheader(f"{emoji} Resultado: suspeita {nivel}")
            st.progress(pontos / 100)
            st.metric("Nível de suspeita", f"{pontos}%")

            st.markdown(f'<div class="result-box"><b>{resumo}</b></div>', unsafe_allow_html=True)

            st.subheader("🔍 Indícios encontrados")
            for motivo in motivos:
                st.write(f"• {motivo}")

# ---------- IMAGEM ----------
elif tipo == "🖼️ Imagem":
    st.header("🖼️ Analisar imagem")
    st.write("Envie uma imagem para uma análise básica de características do arquivo.")

    arquivo = st.file_uploader(
        "Escolha uma imagem",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if arquivo:
        st.image(arquivo, caption="Imagem enviada", use_container_width=True)

        if st.button("🔎 Analisar imagem", use_container_width=True):
            pontos, nivel, emoji, resumo, motivos, dimensoes, hash_arquivo, imagem = analisar_imagem(arquivo)

            st.subheader(f"{emoji} Resultado: suspeita {nivel}")
            st.progress(pontos / 100)
            st.metric("Nível de suspeita", f"{pontos}%")

            col1, col2 = st.columns(2)
            col1.metric("Resolução", f"{dimensoes[0]} × {dimensoes[1]}")
            col2.metric("Identificador do arquivo", hash_arquivo)

            st.markdown(f'<div class="result-box"><b>{resumo}</b></div>', unsafe_allow_html=True)

            st.subheader("🔍 Indícios encontrados")
            for motivo in motivos:
                st.write(f"• {motivo}")

# ---------- VÍDEO ----------
elif tipo == "🎥 Vídeo":
    st.header("🎥 Analisar vídeo")
    st.write("Nesta versão escolar, o sistema verifica informações básicas do arquivo.")

    arquivo = st.file_uploader(
        "Escolha um vídeo",
        type=["mp4", "mov", "webm", "avi"]
    )

    if arquivo:
        st.video(arquivo)

        if st.button("🔎 Analisar vídeo", use_container_width=True):
            pontos, nivel, emoji, resumo, motivos, tamanho_mb = analisar_midia(arquivo)

            st.subheader(f"{emoji} Resultado: suspeita {nivel}")
            st.progress(pontos / 100)
            st.metric("Nível de suspeita", f"{pontos}%")
            st.metric("Tamanho do arquivo", f"{tamanho_mb:.2f} MB")

            st.markdown(f'<div class="result-box"><b>{resumo}</b></div>', unsafe_allow_html=True)

            st.subheader("🔍 Indícios encontrados")
            for motivo in motivos:
                st.write(f"• {motivo}")

            st.warning(
                "Para detectar deepfakes de forma real, seria necessário analisar quadros, rosto, "
                "movimento, áudio e outros sinais com modelos especializados."
            )

# ---------- ÁUDIO ----------
else:
    st.header("🔊 Analisar áudio")
    st.write("Nesta versão escolar, o sistema verifica informações básicas do arquivo.")

    arquivo = st.file_uploader(
        "Escolha um áudio",
        type=["mp3", "wav", "ogg", "m4a"]
    )

    if arquivo:
        st.audio(arquivo)

        if st.button("🔎 Analisar áudio", use_container_width=True):
            pontos, nivel, emoji, resumo, motivos, tamanho_mb = analisar_midia(arquivo)

            st.subheader(f"{emoji} Resultado: suspeita {nivel}")
            st.progress(pontos / 100)
            st.metric("Nível de suspeita", f"{pontos}%")
            st.metric("Tamanho do arquivo", f"{tamanho_mb:.2f} MB")

            st.markdown(f'<div class="result-box"><b>{resumo}</b></div>', unsafe_allow_html=True)

            st.subheader("🔍 Indícios encontrados")
            for motivo in motivos:
                st.write(f"• {motivo}")

            st.warning(
                "Para detectar voz sintética de forma real, seria necessário extrair características "
                "do áudio e usar um modelo treinado para detecção de voz gerada por IA."
            )

# ---------- RODAPÉ ----------
st.markdown("---")
st.caption(
    "Projeto educativo — Grupo 2 | IA e conteúdos manipulados | "
    "Use o resultado como um alerta, não como uma prova."
)
