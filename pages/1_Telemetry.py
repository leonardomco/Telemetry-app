import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import fastf1
from fastf1.core import Session
from Leonardo_V2_1_0 import donnees   

# Get language from session state (set in main app)
lang = st.session_state.lang

# Set translation dictionary AND store it in session_state
T = {
    "title": {"Français": "Télémetrie Formule 1", "English": "Formula 1 Telemetry"},
    "year": {"Français": "Année", "English": "Year"},
    "gp": {"Français": "Grand Prix", "English": "Grand Prix"},
    "session": {"Français": "Session", "English": "Session"},
    "driver": {"Français": "Pilote", "English": "Driver"},
    "load": {"Français": "Charger les données", "English": "Load data"},

    "ok_year":    {"Français": "Confirmer l'année",        "English": "Confirm Year"},
    "ok_gp":      {"Français": "Confirmer le Grand Prix",  "English": "Confirm Grand Prix"},
    "ok_session": {"Français": "Confirmer la session",     "English": "Confirm Session"},
    "ok_driver":  {"Français": "Confirmer le pilote",      "English": "Confirm Driver"},

    "select_confirm_year": {
        "Français": "Sélectionnez et confirmez une année.",
        "English": "Select and confirm a year."
    },
    "select_confirm_gp": {
        "Français": "Sélectionnez et confirmez un Grand Prix.",
        "English": "Select and confirm a Grand Prix."
    },
    "select_confirm_session": {
        "Français": "Sélectionnez et confirmez une session.",
        "English": "Select and confirm a session."
    },
}
st.session_state.T = T

SESSION_MAP = {
    "FP1": {
        "fastf1": "FP1",
        "English": "Practice 1",
        "Français": "Essais Libres 1",
        "aliases": ["practice 1", "fp1", "p1"]
    },
    "FP2": {
        "fastf1": "FP2",
        "English": "Practice 2",
        "Français": "Essais Libres 2",
        "aliases": ["practice 2", "fp2", "p2"]
    },
    "FP3": {
        "fastf1": "FP3",
        "English": "Practice 3",
        "Français": "Essais Libres 3",
        "aliases": ["practice 3", "fp3", "p3"]
    },
    "Qualifying": {
        "fastf1": "Qualifying",
        "English": "Qualifying",
        "Français": "Qualifications",
        "aliases": ["qualifying", "q"]
    },
    "Sprint Qualifying": {
        "fastf1": "Sprint Qualifying",
        "English": "Sprint Qualifying",
        "Français": "Qualifications Sprint",
        "aliases": ["sprint qualifying", "sprint quali"]
    },
    "Sprint": {
        "fastf1": "Sprint",
        "English": "Sprint",
        "Français": "Sprint",
        "aliases": ["sprint"]
    },
    "Race": {
        "fastf1": "Race",
        "English": "Race",
        "Français": "Course",
        "aliases": ["race", "r"]
    }
}
st.session_state.SESSION_MAP = SESSION_MAP

# -------------------------------------------------------------------------
#  APP CONFIG
# -------------------------------------------------------------------------

st.markdown("<style> .stSelectbox label { color: white; } </style>", unsafe_allow_html=True)

# Initialize state flags
for key, default in {
    "year_ok": False,
    "gp_ok": False,
    "session_ok": False,
    "driver_ok": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# -------------------------------------------------------------------------
#  HELPERS — FastF1 queries
# -------------------------------------------------------------------------
def session_to_fastf1(display_name):
    """Convert UI label (FR/EN) into FastF1's session name."""
    lang = st.session_state.lang
    SESSION_MAP = st.session_state.SESSION_MAP

    for key, data in SESSION_MAP.items():
        if data[lang] == display_name:   # match FR or EN label
            return data["fastf1"]

    # Should never happen
    return display_name

@st.cache_data
def get_gp_list(year):
    """Return list of event names for selected year."""
    try:
        events = fastf1.get_event_schedule(year)
        return events['EventName'].tolist()
    except:
        return []

def get_session_list(year, gp_name):
    """Extract session names cleanly from fastf1 event schedule."""
    try:
        events = fastf1.get_event_schedule(year)
        if gp_name not in events['EventName'].values:
            return []

        row = events.loc[events['EventName'] == gp_name].iloc[0]

        session_labels = []

        # Extract session names from columns
        for col in [c for c in row.index if c.startswith("Session") and c.endswith("Name")]:
            val = row[col]
            if pd.isna(val):
                continue
            s = str(val).strip()
            if s:
                session_labels.append(s)

        # Fallback extraction
        if not session_labels:
            for col in [c for c in row.index if c.startswith("Session") and not c.endswith("Name")]:
                val = row[col]
                if pd.isna(val):
                    continue
                if hasattr(val, "tz") or hasattr(val, "hour"):
                    continue
                s = str(val).strip()
                if s and any(ch.isalpha() for ch in s):
                    session_labels.append(s)

        # Normalize names to English codes
        cleaned = []
        for s in session_labels:
            low = s.lower()
            for key, data in SESSION_MAP.items():
                if low in data["aliases"]:
                    cleaned.append(key)
                    break

        # Translate for UI
        lang = st.session_state.lang
        translated = [SESSION_MAP[k][lang] for k in cleaned]

        return translated

    except Exception as e:
        st.error(f"Erreur dans get_session_list: {e}")
        return []

def get_driver_list(year, gp_name, session_name):
    session_fastf1 = session_to_fastf1(session_name)
    ses = fastf1.get_session(year, gp_name, session_fastf1)
    ses.load(laps=False, telemetry=False, weather=False, messages=False)

    codes = []
    for num in ses.drivers:
        info = ses.get_driver(num)
        code = info.get("Abbreviation", None)
        if code:
            codes.append(code)

    return sorted(list(set(codes)))

# -------------------------------------------------------------------------
#  NEW TOP CONTAINER WITH ALL CONTROLS
# -------------------------------------------------------------------------

with st.container():

    # Title
    st.title(T["title"][lang])

    # --- YEAR SELECT ---
    year = st.selectbox(T["year"][lang], list(range(2018, 2026)), key="year")

    if st.button(T["ok_year"][lang]):
        st.session_state.year_ok = True
        st.session_state.gp_ok = False
        st.session_state.session_ok = False
        st.session_state.driver_ok = False

    if not st.session_state.year_ok:
        st.info(T["select_confirm_year"][lang])
        st.stop()

    # --- GRAND PRIX ---
    gp_list = get_gp_list(year)
    gp_name = st.selectbox(T["gp"][lang], gp_list, key="gp")

    if st.button(T["ok_gp"][lang]):
        st.session_state.gp_ok = True
        st.session_state.session_ok = False
        st.session_state.driver_ok = False

    if not st.session_state.gp_ok:
        st.info(T["select_confirm_gp"][lang])
        st.stop()

    # --- SESSION ---
    session_list = get_session_list(year, gp_name)
    session_name = st.selectbox(T["session"][lang], session_list, key="session")

    if st.button(T["ok_session"][lang]):
        st.session_state.session_ok = True
        st.session_state.driver_ok = False

    if not st.session_state.session_ok:
        st.info(T["select_confirm_session"][lang])
        st.stop()

    # --- DRIVER ---
    drivers = get_driver_list(year, gp_name, session_name)

    pilote_code = st.selectbox(
        T["driver"][lang],
        drivers,
        key=f"driver_{year}_{gp_name}_{session_name}"
    )

    if st.button(T["ok_driver"][lang]):
        st.session_state.driver_ok = True
        st.session_state.pilote_code = pilote_code

    if not st.session_state.driver_ok:
        st.stop()

    # --- LOAD BUTTON ---
    load_btn = st.button(T["load"][lang])

# -------------------------------------------------------------------------
#  DATA LOADING + MAIN DISPLAY
# -------------------------------------------------------------------------
if load_btn:
    pilote = st.session_state["pilote_code"]

    # Convert French → English for FastF1
    session_fastf1 = session_to_fastf1(session_name)

    ses = fastf1.get_session(year, gp_name, session_fastf1)

    ses.load(laps=False, telemetry=False)

    driver_number = None
    for num in ses.drivers:
        info = ses.get_driver(num)
        if info["Abbreviation"] == pilote_code:
            driver_number = info["DriverNumber"]
            break

    if driver_number is None:
        st.error(f"Impossible de trouver le pilote '{pilote_code}'")
        st.stop()

    pilote = driver_number

    st.write(f"### {year} ▸ {gp_name} ▸ {session_name} ▸ {pilote_code}")

    with st.spinner("Chargement des données..."):
        try:
            data, track, circuit_info, df_corners = donnees(
                year, gp_name, session_fastf1, pilote
            )

            st.success("✅ Données chargées avec succès")

            # -----------------------------------------------------------------
            #  TRAJECTOIRE (track map)
            # -----------------------------------------------------------------
            X = track[:, 0]
            Y = track[:, 1]

            st.subheader('Trajectoire')
            fig_traj = go.Figure()

            fig_traj.add_trace(go.Scatter(
                x=X,
                y=Y,
                mode='lines',
                line=dict(color='blue', width=2),
                showlegend=False,
            ))

            show_corners = True
            if show_corners and hasattr(circuit_info, "corners"):
                offset_vector = np.array([500, 0])  

                def rotate(xy, *, angle):
                    rot_mat = np.array([
                        [np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]
                    ])
                    return np.matmul(xy, rot_mat)

                track_angle = circuit_info.rotation / 180 * np.pi

                for _, corner in circuit_info.corners.iterrows():
                    txt = f"{corner['Number']}{corner['Letter']}"
                    offset_angle = corner['Angle'] / 180 * np.pi

                    offset_x, offset_y = rotate(offset_vector, angle=offset_angle)
                    text_x = corner['X'] + offset_x
                    text_y = corner['Y'] + offset_y

                    text_x, text_y = rotate(np.array([text_x, text_y]), angle=track_angle)
                    track_x, track_y = rotate(np.array([corner['X'], corner['Y']]), angle=track_angle)

                    fig_traj.add_trace(go.Scatter(
                        x=[track_x, text_x],
                        y=[track_y, text_y],
                        mode="lines",
                        line=dict(color="gray", width=1),
                        showlegend=False
                    ))

                    fig_traj.add_trace(go.Scatter(
                        x=[text_x],
                        y=[text_y],
                        mode="markers+text",
                        marker=dict(size=14, color="gray"),
                        text=[txt],
                        textposition="middle center",
                        textfont=dict(color="white", size=10),
                        showlegend=False
                    ))

            fig_traj.update_layout(
                xaxis_title="Coordonnées X",
                yaxis_title="Coordonnées Y",
                width=800,
                height=600
            )

            fig_traj.update_yaxes(scaleanchor="x", scaleratio=1)

            st.plotly_chart(fig_traj, use_container_width=True)

            # -----------------------------------------------------------------
            #  ALTITUDE
            # -----------------------------------------------------------------
            st.subheader("Altitude")

            fig_alt = go.Figure()
            fig_alt.add_trace(go.Scatter(
                x=data["Distance"],
                y=data["Altitude"],
                mode='lines',
                line=dict(color='blue', width=2),
                name='Altitude'
            ))

            for _, row in df_corners.iterrows():
                fig_alt.add_vline(
                    x=row["Distance"],
                    line=dict(color="white", dash="dash", width=1),
                    opacity=1
                )
                fig_alt.add_annotation(
                    x=row["Distance"],
                    y=min(data["Altitude"]) - 20,
                    text=str(int(row["Number"])),
                    showarrow=False,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=16, color="white"),
                )

            fig_alt.update_layout(
                xaxis_title="Distance (m)",
                yaxis_title="Altitude (m)",
                width=800,
                height=600,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            fig_alt.update_traces(
                hovertemplate="Distance: %{x:.1f} m<br>Altitude: %{y:.1f} m<extra></extra>"
            )

            st.plotly_chart(fig_alt, use_container_width=True)

            # -----------------------------------------------------------------
            #  VITESSE
            # -----------------------------------------------------------------
            st.subheader("Vitesse")

            fig_vit = go.Figure()
            vx_ms = data["vx"]

            fig_vit.add_trace(go.Scatter(
                x=data["Distance"],
                y=vx_ms,
                mode="lines",
                line=dict(color="blue", width=2),
                yaxis="y1"
            ))

            for _, row in df_corners.iterrows():
                fig_vit.add_vline(
                    x=row["Distance"],
                    line=dict(color="white", dash="dash", width=1),
                    opacity=1
                )
                fig_vit.add_annotation(
                    x=row["Distance"],
                    y=min(vx_ms) - 10,
                    text=str(int(row["Number"])),
                    showarrow=False,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=14, color="white")
                )

            fig_vit.update_layout(
                xaxis_title="Distance (m)",
                yaxis_title="Vitesse (m/s)",
                width=800,
                height=600,
                hovermode='x unified',
                plot_bgcolor="rgba(0,0,0,0)"
            )

            fig_vit.update_traces(
                hovertemplate="Distance: %{x:.1f} m<br>Vitesse: %{y:.1f} m/s<extra></extra>"
            )

            st.plotly_chart(fig_vit, use_container_width=True)

            # -----------------------------------------------------------------
            #  ACCÉLÉRATION TANGENTIELLE
            # -----------------------------------------------------------------
            st.subheader("Accélération tangentielle")

            fig_a_t = go.Figure()

            fig_a_t.add_trace(go.Scatter(
                x=data["Distance"],
                y=data["Accélération tangentielle"],
                mode='lines',
                line=dict(color='blue', width=2),
                name='A_t'
            ))

            for _, row in df_corners.iterrows():
                fig_a_t.add_vline(
                    x=row["Distance"],
                    line=dict(color="white", dash="dash", width=1),
                    opacity=1
                )
                fig_a_t.add_annotation(
                    x=row["Distance"],
                    y=min(data["Accélération tangentielle"]) - 20,
                    text=str(int(row["Number"])),
                    showarrow=False,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=16, color="white")
                )

            fig_a_t.update_layout(
                xaxis_title="Distance (m)",
                yaxis_title="Accélération tangentielle (m/s²)",
                width=800,
                height=600,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            fig_a_t.update_traces(
                hovertemplate="Distance: %{x:.1f} m<br>A_t: %{y:.1f} m/s²<extra></extra>"
            )

            st.plotly_chart(fig_a_t, use_container_width=True)

            # -----------------------------------------------------------------
            #  ACCÉLÉRATION NORMALE
            # -----------------------------------------------------------------
            st.subheader("Accélération normale")

            fig_a_n = go.Figure()

            fig_a_n.add_trace(go.Scatter(
                x=data["Distance"],
                y=data["Accélération normale"],
                mode='lines',
                line=dict(color='blue', width=2),
                name='A_n'
            ))

            for _, row in df_corners.iterrows():
                fig_a_n.add_vline(
                    x=row["Distance"],
                    line=dict(color="white", dash="dash", width=1),
                    opacity=1
                )
                fig_a_n.add_annotation(
                    x=row["Distance"],
                    y=min(data["Accélération normale"]) - 20,
                    text=str(int(row["Number"])),
                    showarrow=False,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=16, color="white")
                )

            fig_a_n.update_layout(
                xaxis_title="Distance (m)",
                yaxis_title="Accélération normale (m/s²)",
                width=800,
                height=600,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            fig_a_n.update_traces(
                hovertemplate="Distance: %{x:.1f} m<br>A_n: %{y:.1f} m/s²<extra></extra>"
            )

            st.plotly_chart(fig_a_n, use_container_width=True)

            # -----------------------------------------------------------------
            #  ACCÉLÉRATION VERTICALE
            # -----------------------------------------------------------------
            st.subheader("Accélération verticale")

            fig_a_v = go.Figure()

            fig_a_v.add_trace(go.Scatter(
                x=data["Distance"],
                y=data["Accélération verticale"],
                mode='lines',
                line=dict(color='blue', width=2),
                name='A_v'
            ))

            for _, row in df_corners.iterrows():
                fig_a_v.add_vline(
                    x=row["Distance"],
                    line=dict(color="white", dash="dash", width=1),
                    opacity=1
                )
                fig_a_v.add_annotation(
                    x=row["Distance"],
                    y=min(data["Accélération verticale"]) - 20,
                    text=str(int(row["Number"])),
                    showarrow=False,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=16, color="white")
                )

            fig_a_v.update_layout(
                xaxis_title="Distance (m)",
                yaxis_title="Accélération verticale (m/s²)",
                width=800,
                height=600,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)'
            )

            fig_a_v.update_traces(
                hovertemplate="Distance: %{x:.1f} m<br>A_v: %{y:.1f} m/s²<extra></extra>"
            )

            st.plotly_chart(fig_a_v, use_container_width=True)

            # -----------------------------------------------------------------
            #  PORTANCE
            # -----------------------------------------------------------------
            st.subheader("Portance")

            fig_portance = go.Figure()

            # Courbe moyenne
            fig_portance.add_trace(go.Scatter(
                x=data["Distance"],
                y=data["Portance_moy"],
                mode='lines',
                line=dict(color='blue', width=2),
                name='Portance moyenne'
            ))

            # Zone min-max
            fig_portance.add_trace(go.Scatter(
                x=pd.concat([data["Distance"], data["Distance"][::-1]]),
                y=pd.concat([data["Portance_max"], data["Portance_min"][::-1]]),
                fill='toself',
                fillcolor='rgba(0, 0, 255, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='min–max',
                showlegend=False
            ))

            for _, row in df_corners.iterrows():
                fig_portance.add_vline(
                    x=row["Distance"],
                    line=dict(color="white", dash="dash", width=1),
                    opacity=1
                )
                fig_portance.add_annotation(
                    x=row["Distance"],
                    y=min(data["Portance_min"]) - 20,
                    text=str(int(row["Number"])),
                    showarrow=False,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=16, color="white")
                )

            fig_portance.update_layout(
                xaxis_title="Distance (m)",
                yaxis_title="Portance (N)",
                width=800,
                height=600,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )

            fig_portance.update_traces(
                hovertemplate="Distance: %{x:.1f} m<br>Portance: %{y:.1f} N<extra></extra>"
            )

            st.plotly_chart(fig_portance, use_container_width=True)

            # -----------------------------------------------------------------
            #  TRAÎNÉE
            # -----------------------------------------------------------------
            st.subheader("Trainée")

            fig_trainee = go.Figure()

            fig_trainee.add_trace(go.Scatter(
                x=data["Distance"],
                y=data["Trainée_moy"],
                mode='lines',
                line=dict(color='blue', width=2),
                name='Trainée moyenne'
            ))

            fig_trainee.add_trace(go.Scatter(
                x=pd.concat([data["Distance"], data["Distance"][::-1]]),
                y=pd.concat([data["Trainée_max"], data["Trainée_min"][::-1]]),
                fill='toself',
                fillcolor='rgba(0, 0, 255, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='min–max',
                showlegend=False
            ))

            for _, row in df_corners.iterrows():
                fig_trainee.add_vline(
                    x=row["Distance"],
                    line=dict(color="white", dash="dash", width=1),
                    opacity=1
                )
                fig_trainee.add_annotation(
                    x=row["Distance"],
                    y=min(data["Trainée_min"]) - 20,
                    text=str(int(row["Number"])),
                    showarrow=False,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=16, color="white")
                )

            fig_trainee.update_layout(
                xaxis_title="Distance (m)",
                yaxis_title="Trainée (N)",
                width=800,
                height=600,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )

            fig_trainee.update_traces(
                hovertemplate="Distance: %{x:.1f} m<br>Trainée: %{y:.1f} N<extra></extra>"
            )

            st.plotly_chart(fig_trainee, use_container_width=True)

            # -----------------------------------------------------------------
            #  FORCE DE FROTTEMENT DE ROULEMENT
            # -----------------------------------------------------------------
            st.subheader("Force de frottement au roulement")

            fig_fr = go.Figure()

            fig_fr.add_trace(go.Scatter(
                x=data["Distance"],
                y=data["Force de frottement de roulement moy"],
                mode='lines',
                line=dict(color='blue', width=2),
                name='Frottement moy'
            ))

            fig_fr.add_trace(go.Scatter(
                x=pd.concat([data["Distance"], data["Distance"][::-1]]),
                y=pd.concat([data["Force de frottement de roulement max"],
                             data["Force de frottement de roulement min"][::-1]]),
                fill='toself',
                fillcolor='rgba(0, 0, 255, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                showlegend=False
            ))

            for _, row in df_corners.iterrows():
                fig_fr.add_vline(
                    x=row["Distance"],
                    line=dict(color="white", dash="dash", width=1),
                    opacity=1
                )
                fig_fr.add_annotation(
                    x=row["Distance"],
                    y=min(data["Force de frottement de roulement min"]) - 20,
                    text=str(int(row["Number"])),
                    showarrow=False,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=16, color="white")
                )

            fig_fr.update_layout(
                xaxis_title="Distance (m)",
                yaxis_title="Frottement de roulement (N)",
                width=800,
                height=600,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )

            fig_fr.update_traces(
                hovertemplate="Distance: %{x:.1f} m<br>Frottement: %{y:.1f} N<extra></extra>"
            )

            st.plotly_chart(fig_fr, use_container_width=True)

            # -----------------------------------------------------------------
            #  FORCE MOTRICE
            # -----------------------------------------------------------------
            st.subheader("Force motrice")

            fig_m = go.Figure()

            fig_m.add_trace(go.Scatter(
                x=data["Distance"],
                y=data["Force motrice moy"],
                mode='lines',
                line=dict(color='blue', width=2),
                name='Force motrice moy'
            ))

            fig_m.add_trace(go.Scatter(
                x=pd.concat([data["Distance"], data["Distance"][::-1]]),
                y=pd.concat([data["Force motrice max"],
                             data["Force motrice min"][::-1]]),
                fill='toself',
                fillcolor='rgba(0, 0, 255, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                showlegend=False
            ))

            for _, row in df_corners.iterrows():
                fig_m.add_vline(
                    x=row["Distance"],
                    line=dict(color="white", dash="dash", width=1),
                    opacity=1
                )
                fig_m.add_annotation(
                    x=row["Distance"],
                    y=min(data["Force motrice min"]) - 20,
                    text=str(int(row["Number"])),
                    showarrow=False,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=16, color="white")
                )

            fig_m.update_layout(
                xaxis_title="Distance (m)",
                yaxis_title="Force motrice (N)",
                width=800,
                height=600,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )

            fig_m.update_traces(
                hovertemplate="Distance: %{x:.1f} m<br>Force motrice: %{y:.1f} N<extra></extra>"
            )

            st.plotly_chart(fig_m, use_container_width=True)

            # -----------------------------------------------------------------
            #  FORCE DE FREINAGE
            # -----------------------------------------------------------------
            st.subheader("Force de freinage")

            fig_f = go.Figure()

            fig_f.add_trace(go.Scatter(
                x=data["Distance"],
                y=data["Force de freinage moy"],
                mode='lines',
                line=dict(color='blue', width=2),
                name='Freinage moy'
            ))

            fig_f.add_trace(go.Scatter(
                x=pd.concat([data["Distance"], data["Distance"][::-1]]),
                y=pd.concat([data["Force de freinage max"],
                            data["Force de freinage min"][::-1]]),
                fill='toself',
                fillcolor='rgba(0, 0, 255, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                showlegend=False
            ))

            for _, row in df_corners.iterrows():
                fig_f.add_vline(
                    x=row["Distance"],
                    line=dict(color="white", dash="dash", width=1),
                    opacity=1
                )
                fig_f.add_annotation(
                    x=row["Distance"],
                    y=min(data["Force de freinage min"]) - 20,
                    text=str(int(row["Number"])),
                    showarrow=False,
                    xanchor="center",
                    yanchor="top",
                    font=dict(size=16, color="white")
                )

            fig_f.update_layout(
                xaxis_title="Distance (m)",
                yaxis_title="Force de freinage (N)",
                width=800,
                height=600,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )

            fig_f.update_traces(
                hovertemplate="Distance: %{x:.1f} m<br>Freinage: %{y:.1f} N<extra></extra>"
            )

            st.plotly_chart(fig_f, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Erreur lors du chargement ou de l'affichage des données : {e}")




