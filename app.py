import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import os
from datetime import datetime
import hashlib

# ── Configuration ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DigiStudy · Enquête Numérique",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = "digistudy.db"

# ── CSS Custom ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background: #0a0a0f;
    color: #e8e6f0;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    letter-spacing: -0.03em;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #c8b8ff 0%, #ff8fcf 50%, #8ff5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}

.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #7a7a9a;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.card {
    background: linear-gradient(135deg, #13131f 0%, #1a1a2e 100%);
    border: 1px solid #2a2a4a;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.stat-card {
    background: linear-gradient(135deg, #1e1e35 0%, #16162a 100%);
    border: 1px solid #3a2a6a;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}

.stat-number {
    font-family: 'Space Mono', monospace;
    font-size: 2.5rem;
    font-weight: 700;
    color: #c8b8ff;
    line-height: 1;
}

.stat-label {
    font-size: 0.75rem;
    color: #7a7a9a;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.4rem;
}

.tag {
    display: inline-block;
    background: #2a1f5a;
    color: #c8b8ff;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    margin: 0.2rem;
}

.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #c8b8ff;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    border-left: 3px solid #c8b8ff;
    padding-left: 0.8rem;
    margin-bottom: 1rem;
}

.success-box {
    background: linear-gradient(135deg, #0f2a1a, #162a20);
    border: 1px solid #2a6a3a;
    border-radius: 12px;
    padding: 1.2rem;
    color: #8ff5c1;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
}

div[data-testid="stSidebar"] {
    background: #0d0d1a;
    border-right: 1px solid #1e1e35;
}

.stButton > button {
    background: linear-gradient(135deg, #6a3aff, #c83aaa);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 0.6rem 2rem;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(106, 58, 255, 0.4);
}

.stSelectbox > div, .stMultiSelect > div {
    background: #13131f;
    border-color: #2a2a4a;
}

.stSlider > div {
    color: #c8b8ff;
}

hr {
    border-color: #2a2a4a;
}
</style>
""", unsafe_allow_html=True)

# ── Base de données ─────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS reponses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            horodatage TEXT,
            age INTEGER,
            genre TEXT,
            filiere TEXT,
            niveau TEXT,
            heures_ecran REAL,
            heures_reseaux REAL,
            plateformes TEXT,
            usage_dominant TEXT,
            appareil_principal TEXT,
            connexion_qualite TEXT,
            cours_en_ligne INTEGER,
            satisfaction_num INTEGER,
            stress_numerique INTEGER,
            teletravail_pref TEXT,
            competences_auto INTEGER,
            outils_travail TEXT,
            score_hash TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_response(data: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    h = hashlib.md5(str(data).encode()).hexdigest()[:8]
    c.execute("""
        INSERT INTO reponses (
            horodatage, age, genre, filiere, niveau,
            heures_ecran, heures_reseaux, plateformes, usage_dominant,
            appareil_principal, connexion_qualite, cours_en_ligne,
            satisfaction_num, stress_numerique, teletravail_pref,
            competences_auto, outils_travail, score_hash
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        datetime.now().isoformat(),
        data["age"], data["genre"], data["filiere"], data["niveau"],
        data["heures_ecran"], data["heures_reseaux"],
        ",".join(data["plateformes"]), data["usage_dominant"],
        data["appareil_principal"], data["connexion_qualite"],
        data["cours_en_ligne"], data["satisfaction_num"],
        data["stress_numerique"], data["teletravail_pref"],
        data["competences_auto"], ",".join(data["outils_travail"]), h
    ))
    conn.commit()
    conn.close()
    return h

def load_data() -> pd.DataFrame:
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM reponses", conn)
    conn.close()
    return df

# ── Init ───────────────────────────────────────────────────────────────────────
init_db()

# ── Sidebar Navigation ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 0.5rem 0;">
        <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#7a7a9a; letter-spacing:0.2em; text-transform:uppercase;">Navigation</div>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio("", [
        "📡  Accueil",
        "📝  Formulaire",
        "📊  Tableau de bord",
        "🔬  Analyse avancée",
        "📥  Données brutes"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    df_check = load_data()
    n = len(df_check)
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{n}</div>
        <div class="stat-label">réponses collectées</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top:2rem; font-family:'Space Mono',monospace; font-size:0.65rem; color:#3a3a5a; text-align:center;">
        DigiStudy v1.0 · INF232 EC2<br>TP Collecte & Analyse
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# PAGE : ACCUEIL
# ════════════════════════════════════════════════════════════════════════════════
if "Accueil" in page:
    st.markdown('<div class="hero-title">DigiStudy</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">📡 Enquête sur les habitudes numériques des étudiants</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <p style="color:#b8b6d0; font-size:1rem; line-height:1.7;">
        Cette plateforme collecte et analyse les <strong style="color:#c8b8ff">habitudes numériques des étudiants</strong> — 
        temps d'écran, usages des réseaux sociaux, outils de travail, qualité de connexion — 
        pour produire des <strong style="color:#ff8fcf">statistiques descriptives</strong> en temps réel.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("📝", "Formulaire", "18 questions structurées"),
        ("📊", "Visualisation", "Graphiques interactifs"),
        ("🔬", "Analyse", "Stats descriptives complètes"),
        ("💾", "Persistance", "Base SQLite locale"),
    ]
    for col, (icon, title, desc) in zip([col1,col2,col3,col4], metrics):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:1.8rem">{icon}</div>
                <div style="font-weight:700; color:#e8e6f0; margin-top:0.5rem">{title}</div>
                <div class="stat-label">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="section-header">Thèmes couverts</div>', unsafe_allow_html=True)
    tags = ["Temps d'écran", "Réseaux sociaux", "Cours en ligne", "Outils numériques", 
            "Qualité de connexion", "Stress numérique", "Télétravail", "Auto-formation"]
    tags_html = "".join([f'<span class="tag">{t}</span>' for t in tags])
    st.markdown(tags_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# PAGE : FORMULAIRE
# ════════════════════════════════════════════════════════════════════════════════
elif "Formulaire" in page:
    st.markdown('<div class="hero-title" style="font-size:2rem">Formulaire</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Remplissez toutes les sections · Données anonymisées</div>', unsafe_allow_html=True)
    
    with st.form("enquete_form", clear_on_submit=True):
        
        # ── Section 1 : Profil ──
        st.markdown('<div class="section-header">01 · Profil étudiant</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            age = st.number_input("Âge", min_value=16, max_value=40, value=20)
        with c2:
            genre = st.selectbox("Genre", ["Homme", "Femme", "Non-binaire", "Préfère ne pas dire"])
        with c3:
            filiere = st.selectbox("Filière", [
                "Informatique", "Mathématiques", "Physique", "Économie",
                "Droit", "Médecine", "Lettres", "Sciences Sociales", "Autre"
            ])
        with c4:
            niveau = st.selectbox("Niveau", ["Licence 1", "Licence 2", "Licence 3", "Master 1", "Master 2", "Doctorat"])
        
        st.markdown("---")
        
        # ── Section 2 : Temps d'écran ──
        st.markdown('<div class="section-header">02 · Temps d\'écran quotidien</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            heures_ecran = st.slider("Temps total sur écran (heures/jour)", 0.0, 18.0, 6.0, 0.5)
        with c2:
            heures_reseaux = st.slider("Dont réseaux sociaux (heures/jour)", 0.0, 10.0, 2.0, 0.5)
        
        st.markdown("---")
        
        # ── Section 3 : Usages ──
        st.markdown('<div class="section-header">03 · Usages numériques</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            plateformes = st.multiselect("Réseaux sociaux utilisés", 
                ["Instagram", "TikTok", "Facebook", "Twitter/X", "LinkedIn", 
                 "YouTube", "Snapchat", "WhatsApp", "Telegram", "Discord"],
                default=["Instagram", "WhatsApp"])
            usage_dominant = st.selectbox("Usage numérique dominant", [
                "Études / Recherche", "Divertissement", "Communication", 
                "Jeux vidéo", "Création de contenu", "Shopping", "Travail"
            ])
        with c2:
            appareil_principal = st.selectbox("Appareil principal", 
                ["Smartphone", "Laptop", "Ordinateur fixe", "Tablette"])
            connexion_qualite = st.selectbox("Qualité de votre connexion internet", 
                ["Excellente (fibre)", "Bonne (ADSL/4G)", "Moyenne", "Mauvaise", "Très instable"])
        
        st.markdown("---")
        
        # ── Section 4 : Formation ──
        st.markdown('<div class="section-header">04 · Formation & outils</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            cours_en_ligne = st.slider("Cours en ligne suivis cette année", 0, 20, 3)
            competences_auto = st.slider("Compétences auto-apprises en ligne (0=aucune, 10=beaucoup)", 0, 10, 5)
        with c2:
            outils_travail = st.multiselect("Outils numériques de travail utilisés",
                ["Google Docs", "Notion", "VS Code", "Jupyter", "ChatGPT/IA", 
                 "Canva", "Excel/Sheets", "Moodle", "Zoom/Meet", "GitHub"],
                default=["Google Docs", "Moodle"])
            teletravail_pref = st.selectbox("Préférez-vous étudier/travailler en...",
                ["Présentiel uniquement", "Distanciel uniquement", "Hybride (mix)", "Indifférent"])
        
        st.markdown("---")
        
        # ── Section 5 : Bien-être ──
        st.markdown('<div class="section-header">05 · Bien-être numérique</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            satisfaction_num = st.slider("Satisfaction globale envers votre vie numérique (1-10)", 1, 10, 6)
        with c2:
            stress_numerique = st.slider("Niveau de stress lié au numérique (1-10)", 1, 10, 4)
        
        st.markdown("---")
        submitted = st.form_submit_button("📡  Soumettre mes réponses", use_container_width=True)
        
        if submitted:
            if len(plateformes) == 0:
                st.error("Sélectionnez au moins un réseau social.")
            elif heures_reseaux > heures_ecran:
                st.error("Le temps sur réseaux sociaux ne peut pas dépasser le temps total sur écran.")
            else:
                data = {
                    "age": age, "genre": genre, "filiere": filiere, "niveau": niveau,
                    "heures_ecran": heures_ecran, "heures_reseaux": heures_reseaux,
                    "plateformes": plateformes, "usage_dominant": usage_dominant,
                    "appareil_principal": appareil_principal, "connexion_qualite": connexion_qualite,
                    "cours_en_ligne": cours_en_ligne, "satisfaction_num": satisfaction_num,
                    "stress_numerique": stress_numerique, "teletravail_pref": teletravail_pref,
                    "competences_auto": competences_auto, "outils_travail": outils_travail
                }
                code = save_response(data)
                st.markdown(f"""
                <div class="success-box">
                ✅ Réponse enregistrée avec succès !<br>
                Code de participation : <strong>#{code}</strong><br>
                Merci pour votre contribution à l'enquête DigiStudy.
                </div>
                """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# PAGE : TABLEAU DE BORD
# ════════════════════════════════════════════════════════════════════════════════
elif "Tableau de bord" in page:
    st.markdown('<div class="hero-title" style="font-size:2rem">Tableau de bord</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Statistiques descriptives · Temps réel</div>', unsafe_allow_html=True)
    
    df = load_data()
    
    if df.empty:
        st.info("Aucune donnée disponible. Remplissez le formulaire d'abord !")
    else:
        n = len(df)
        c1, c2, c3, c4, c5 = st.columns(5)
        stats = [
            (n, "Répondants"),
            (f"{df['heures_ecran'].mean():.1f}h", "Moy. écran/jour"),
            (f"{df['heures_reseaux'].mean():.1f}h", "Moy. réseaux/jour"),
            (f"{df['satisfaction_num'].mean():.1f}/10", "Satisfaction num."),
            (f"{df['stress_numerique'].mean():.1f}/10", "Stress numérique"),
        ]
        for col, (val, label) in zip([c1,c2,c3,c4,c5], stats):
            with col:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{val}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Row 1
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown('<div class="section-header">Temps d\'écran par filière</div>', unsafe_allow_html=True)
            fig = px.box(df, x="filiere", y="heures_ecran", color="filiere",
                        color_discrete_sequence=px.colors.sequential.Plasma_r)
            fig.update_layout(
                plot_bgcolor="#0d0d1a", paper_bgcolor="#0d0d1a",
                font_color="#b8b6d0", showlegend=False,
                xaxis=dict(tickangle=30, gridcolor="#1e1e35"),
                yaxis=dict(gridcolor="#1e1e35"),
                margin=dict(t=20, b=60)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with c2:
            st.markdown('<div class="section-header">Répartition par genre</div>', unsafe_allow_html=True)
            genre_counts = df["genre"].value_counts().reset_index()
            genre_counts.columns = ["genre", "count"]
            fig = px.pie(genre_counts, names="genre", values="count",
                        color_discrete_sequence=["#c8b8ff","#ff8fcf","#8ff5e1","#ffd97a"],
                        hole=0.5)
            fig.update_layout(
                plot_bgcolor="#0d0d1a", paper_bgcolor="#0d0d1a",
                font_color="#b8b6d0",
                margin=dict(t=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Row 2
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown('<div class="section-header">Appareils principaux</div>', unsafe_allow_html=True)
            ap_counts = df["appareil_principal"].value_counts().reset_index()
            ap_counts.columns = ["appareil", "count"]
            fig = px.bar(ap_counts, x="count", y="appareil", orientation="h",
                        color="count", color_continuous_scale="Purp")
            fig.update_layout(
                plot_bgcolor="#0d0d1a", paper_bgcolor="#0d0d1a",
                font_color="#b8b6d0", showlegend=False, coloraxis_showscale=False,
                xaxis=dict(gridcolor="#1e1e35"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)"),
                margin=dict(t=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with c2:
            st.markdown('<div class="section-header">Satisfaction vs Stress (scatter)</div>', unsafe_allow_html=True)
            fig = px.scatter(df, x="satisfaction_num", y="stress_numerique",
                           color="filiere", size="heures_ecran",
                           hover_data=["genre", "niveau"],
                           color_discrete_sequence=px.colors.qualitative.Vivid)
            fig.update_layout(
                plot_bgcolor="#0d0d1a", paper_bgcolor="#0d0d1a",
                font_color="#b8b6d0",
                xaxis=dict(gridcolor="#1e1e35", title="Satisfaction"),
                yaxis=dict(gridcolor="#1e1e35", title="Stress"),
                margin=dict(t=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Plateformes
        st.markdown('<div class="section-header">Popularité des plateformes sociales</div>', unsafe_allow_html=True)
        all_platforms = []
        for row in df["plateformes"].dropna():
            all_platforms.extend(row.split(","))
        if all_platforms:
            plat_series = pd.Series(all_platforms).value_counts().reset_index()
            plat_series.columns = ["plateforme", "count"]
            fig = px.bar(plat_series, x="plateforme", y="count",
                        color="count", color_continuous_scale="Purples",
                        text="count")
            fig.update_layout(
                plot_bgcolor="#0d0d1a", paper_bgcolor="#0d0d1a",
                font_color="#b8b6d0", coloraxis_showscale=False,
                xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                yaxis=dict(gridcolor="#1e1e35"),
                margin=dict(t=20)
            )
            st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# PAGE : ANALYSE AVANCÉE
# ════════════════════════════════════════════════════════════════════════════════
elif "Analyse avancée" in page:
    st.markdown('<div class="hero-title" style="font-size:2rem">Analyse avancée</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Corrélations & tendances</div>', unsafe_allow_html=True)

    df = load_data()

    if df.empty:
        st.info("Aucune donnée disponible.")
    else:
        corr = df[["heures_ecran", "heures_reseaux", "satisfaction_num", "stress_numerique"]].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="Purples",
            aspect="auto"
        )
        fig.update_layout(
            plot_bgcolor="#0d0d1a",
            paper_bgcolor="#0d0d1a",
            font_color="#b8b6d0",
            margin=dict(t=20)
        )
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# PAGE : DONNÉES BRUTES
# ════════════════════════════════════════════════════════════════════════════════
elif "Données brutes" in page:
    st.markdown('<div class="hero-title" style="font-size:2rem">Données brutes</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Vue tabulaire des réponses</div>', unsafe_allow_html=True)

    df = load_data()

    if df.empty:
        st.info("Aucune donnée disponible.")
    else:
        st.dataframe(df, use_container_width=True)
