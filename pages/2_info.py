import streamlit as st
import pandas as pd

lang = st.session_state.lang

st.title("Informations concernant les données présentées")

st.markdown("## Table des matières")
st.markdown("""
- [1. Grandeurs physiques](#1-grandeurs-physiques)
- [2. Approximations réalisées](#2-approximations-réalisées)
- [3. Estimations des coefficients et leur limites](#3-estimations-des-coefficients-et-leur-limites)
- [4. Traitement des données](#4-traitement-des-données)
""")

st.markdown("## 1. Grandeurs physiques")

# ──────────────────────────────
st.subheader("Trajectoire")

st.write(
    "La trajectoire est l’ensemble des positions occupées par la voiture de Formule 1 au cours du temps."
)
st.write(
    "Dans le plan, elle est représentée par la courbe d’équation $y(x)$."
)

# ──────────────────────────────
st.subheader("Altitude")

st.write(
    "L'altitude est représentée en prenant le premier point comme point de référence."
)
st.write(
    "Elle est décrite par la fonction $altitude(s)$, où $s$ représente la distance parcourue."
)

# ──────────────────────────────
st.subheader("Vitesse")

st.write(
    "La vitesse présentée est la norme du vecteur vitesse en fonction de la distance parcourue."
)
st.latex(
    r"\lVert \vec{v}(s) \rVert"
)
st.write(
    "Le vecteur vitesse est obtenu par dérivation du vecteur position."
)

# ──────────────────────────────
st.subheader("Accélération tangentielle")

st.write(
    "L’accélération tangentielle est la composante de l’accélération dont la direction est tangente à la trajectoire."
)
st.write(
    "Elle est définie comme la variation de la norme de la vitesse par unité de temps :"
)
st.latex(
    r"a_{\mathrm{t}}(t) = \frac{d\lVert \vec{v}(t) \rVert}{dt} = \frac{dv(t)}{dt}"
)
st.write(
    "Dans les graphiques présentés, l’accélération tangentielle est représentée en fonction de la distance parcourue $s$."
)

# ──────────────────────────────
st.subheader("Accélération normale")

st.write(
    "L’accélération normale est la composante de l’accélération dont la direction est orthogonale à la trajectoire."
)
st.write(
    "Elle est définie comme le produit entre le carré de la vitesse et la courbure :"
)
st.latex(
    r"a_{\mathrm{n}}(t) = v(t)^2\,\gamma"
)

st.write(
    "La courbure peut être définie comme la valeur absolue de la variation de l’angle $\\theta$ "
    "par rapport à la distance parcourue $s$ :"
)
st.latex(
    r"\gamma = \left\lvert \frac{d\theta}{ds} \right\rvert"
)

st.write(
    "Dans le cas d’une trajectoire plane décrite par une fonction $y(x)$, "
    "l’angle $\\theta$ entre la tangente et l’axe $x$ vérifie :"
)
st.latex(
    r"\theta = \arctan\!\left(\frac{dy}{dx}\right)"
)

st.write(
    "Dans les graphiques présentés, l’accélération normale est représentée en fonction de la distance parcourue $s$."
)

# ──────────────────────────────
st.subheader("Accélération verticale")

st.write(
    "L’accélération verticale est la composante de l’accélération suivant l’axe vertical."
)
st.write(
    "Elle est définie de façon analogue à l'accélération normale mais dans le plan $Oxz$."
)
st.write(
    "Il est donc possible de définir la courbure verticale comme : "
)
st.latex(
    r"\gamma_z = \left\lvert \frac{d\theta_z}{ds_z} \right\rvert"
)
st.write(
    "Dans le cas d’une trajectoire sur le plan $Oxz$ décrite par une fonction $z(x)$, "
    "l’angle $\\theta_z$ entre la tangente et l’axe $x$ vérifie :"
)
st.latex(
    r"\theta_z = \arctan\!\left(\frac{dz}{dx}\right)"
)
st.write(
    "L'accélération verticale est donc définie comme :"
)
st.latex(
    r"a_{\mathrm{v}}(t) = v(t)^2\,\gamma_z"
)

st.write(
    "Dans les graphiques présentés, cette accélération est représentée en fonction de la distance parcourue $s$."
)

# ──────────────────────────────
st.subheader("Portance")

st.write(
    "La portance est la composante de la force aérodynamique qui s’exerce perpendiculairement "
    "à la vitesse relative de l’air autour du véhicule."
)
st.write(
    "La norme de cette force est donnée par :"
)
st.latex(
    r"\lVert \vec{F}_L(t) \rVert = \frac{1}{2}\,\rho\,v(t)^2\,A\,C_L"
)
st.write(
    "Dans cette expression, $\\rho$ est la densité de l’air, $A$ l’aire de référence aérodynamique, "
    "$C_L$ le coefficient de portance et $v$ la norme de la vitesse."
)
st.write(
    "Dans les graphiques présentés, sa norme est affichée en fonction de la distance parcourue $s$."
)

# ──────────────────────────────
st.subheader("Traînée")

st.write(
    "La traînée est la force qui s’oppose au mouvement de la voiture dans l’air."
)
st.write(
    "La norme de cette force est définie par :"
)
st.latex(
    r"\lVert \vec{F}_D(t) \rVert = \frac{1}{2}\,\rho\,v(t)^2\,A\,C_D"
)
st.write(
    "Dans cette expression, $\\rho$ est la densité de l’air, $A$ l’aire frontale, "
    "$C_D$ le coefficient de traînée et $v$ la norme de la vitesse."
)
st.write(
    "Dans les graphiques présentés, sa norme est affichée en fonction de la distance parcourue $s$."
)

# ──────────────────────────────
st.subheader("Force de frottement au roulement")
st.write(
        "Il s'agit de la force de frottement due au contact entre les pneus d'une voiture et la surface, habituellement du goudron. "
)
st.write(
    "La norme de cette force est définie par :"
)
st.latex(
    r"\left\lVert\vec{F}_r (t)\right\rVert = C_{fr}F_s(t)"
)
st.write(
    "Dans cette expression, "
    "$C_{fr}$ est le coefficient de frottement de roulement et $F_s(t)$ est la norme de la la force de soutien qui est la somme de la force de pesanteur et de la portance."
)
st.write(
    "Dans les graphiques présentés, sa norme est affichée en fonction de la distance parcourue $s$."
)

# ──────────────────────────────

st.subheader("Force motrice")
st.write(
        "La force motrice est la force résultant de l'action du moteur qui permet à la voiture de se déplacer dans le sens du déplacement."
)
st.write(
    "La force motrice est définie par partie pour distinguer les phases où le moteur est en marche et où il ne l'est pas."
)
st.write(
    "La norme de cette force est définie par :"
)
st.latex(
    r"""
    \left\lVert \vec{F}_m(t) \right\rVert =
    \begin{cases}
        m\,a_t(t) + F_r(t) + F_D(t),
        & \text{si } a_t > 0 \text{ et que la voiture ne freine pas}, \\[6pt]
        0,
        & \text{si } a_t < 0 \text{ et que la voiture freine}.
    \end{cases}
    """
)


st.write(
    "Dans les graphiques présentés, sa norme est affichée en fonction de la distance parcourue $s$."
)

# ──────────────────────────────
st.subheader("Force de freinage")
st.write(
        "La force de freinage est la force opposée au sens du déplacement qui permet à l'objet de diminuer sa vitesse. " 
)
st.write(
    "Cette force, dépendant de l'action ou non des freins peut être définie comme une fonction par morceaux."
)
st.write(
    "La norme de cette force est définie par :"
)
st.latex(
    r"""
    \left\lVert \vec{F}_{freins}(t) \right \rVert =
    \begin{cases}
        m|a_t(t)| + |F_D(t)| + |F_r(t)| & \text{si } a_t<0 \text{ et que la voiture freine} \\
        0 & \text{si } a_t>0 \text{ et que la voiture ne freine pas}
    \end{cases}
    """
)


st.write(
    "Dans les graphiques présentés, sa norme est affichée en fonction de la distance parcourue $s$."
)


st.markdown("## 2. Approximations réalisées")
st.write(
    "Dans ce travail, plusieurs hypothèses ont dû être réalisées afin de rendre les calculs possibles."
)
st.subheader("Approximation ponctuelle")
st.write(
    "Le véhicule est assimilé à un point, ce qui permet de négliger les moments " \
    "de force, d’inertie et cinétique ainsi que les transferts de charge. Cela permet également " \
    "d’appliquer le principe fondamental de la dynamique."
)
st.subheader("Masse supposées constante")
st.write(
    "La masse est considérée constante dans le temps alors qu’elle diminue normalement à mesure que le " \
    "carburant est utilisé. Cette hypothèse est nécessaire puisque la variation de masse du carburant n’est pas connue."
)
st.subheader("Accélération verticale supposées nulle dans la partie dynamique")
st.write(
    "Cette approximation se justifie par le fait que l’accélération verticale dépend principalement des variations ponctuelles " \
    "de la surface de roulage. En règle générale, elle peut donc être approximée à 0 en dehors de ces irrégularités."
)
st.subheader("Roues supposées libres")
st.write(
    "Cette hypothèse est valable la majeure partie du temps, lorsque les voitures ne freinent pas, et simplifie la" \
    " modélisation de la force de frottement de roulement."
)
st.subheader("Force motrice supposée nulle lors des freinages")
st.write(
    "Cela revient à négliger le frein moteur, car il n’est pas possible de le quantifier."
)


st.markdown("## 3. Estimations des coefficients et leur limites")
st.subheader("Masse des voitures")
st.write(
    "La masse des voitures est calculée à l'aide de la formule suivante : "
)
st.latex(
    r"m = m_{min\; voiture} + \frac{1}{2} m_{max\; carburant} \pm \frac{1}{2} m_{max\; carburant}"
)
st.write("La masse est considérée la même pour toute les voitures et dépend simplement de l'année. Ainsi voici la masse en fonction des années : ")

data = {
    "Année": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "Masse minimale de la voiture (kg)": [733, 743, 746, 752, 798, 798, 798, 800],
    "Masse maximale de carburant (kg)": [105, 110, 110, 110, 110, 110, 110, 110],
    "Masse totale (kg)": [
        "785.5 ± 52.5",
        "798 ± 55",
        "801 ± 55",
        "807 ± 55",
        "853 ± 55",
        "853 ± 55",
        "853 ± 55",
        "855 ± 55",
    ],
}

df = pd.DataFrame(data)

st.subheader("Masse en fonction des années")
st.table(df)
st.write("Les masses minimales sont définies par les règlements FIA")


st.subheader("Masse volumique de l'air")
st.write(
    "La masse volumique de l’air $\\rho$ est définie à l’aide d’une formule empirique "
    "qui l’exprime en fonction de la pression $p$, de la température $T$ "
    "et de l’humidité relative $h$ :"
)
st.latex(r"\rho(h, T, p) = \frac{1}{R_s(T + 273,15)}\bigg(p-230,617 \cdot h\cdot e^{\Big(\frac{17,5043T}{241,2 + T}\Big)}\bigg)")


st.subheader("Coefficients aérodynamiques")
st.write(
    "Les coeffcients aerodynamiques proviennent de plusieurs sources sur internet. Les valeurs sont les mêmes pour toutes les voitures même si cela ne devrait pas être le cas. Voici les valeurs : "

)
st.write("$C_D$ = 1,503")
st.write("$C_L$ = -3,679")
st.write("$A$ = 1 $m^2$")


st.subheader("Coefficient de frottement de roulement")
st.write("Pour le coefficient de frottement de roulement il faut également l'estimer à l'aide de valeurs présentent dans la littérature. ")
st.write("Souvent les valeurs présentées sur internet se situent entre 0,01 et 0,02 je vais donc garder la valeur centrale :")
st.latex(r"C_{fr}= 0,015")
st.subheader("Incertitudes")
st.write("Les coefficients impliquent une incértitude puisqu'ils sont estimés.")
st.write("Pour la masse cela est détaillé plus haut.")
st.write("Pour la masse volumique de l'air je ne vais pas considérer d'incertitude car les données atmosphériques sont précises")
st.write("Pour les coeffcients aérodynamiques, je vais considérer une incertitude de 10%")
st.write("Pour le coefficient de frottement de roulement je vais considérer les valeurs maximales et minimales trouvées pour l'incertitude.")
st.write("Les incertitudes sont présentées sur les graphiques par la zone de couleur ombrée.")

st.markdown("## 4. Traitement des données")
st.write("Les graphiques des trois accélérations sont traités afin de les rendre lisibles et de supprimer le bruit.")
st.write(
    "Le traitement de ces données repose sur un algorithme combinant la substitution des valeurs extrêmes "
    "par les valeurs précédentes et un filtrage de Savitzky–Golay."
)


st.subheader("Paramètrage du traitement des données")

st.write(r"\- Filtre de Savitzky–Golay :")

st.latex(
    r"""
    \begin{aligned}
    &\text{window\_length} = 9 \quad \text{pour } a_t \\
    &\text{window\_length} = 13 \quad \text{pour } a_n \\
    &\text{window\_length} = 21 \quad \text{pour } a_v \\
    &\text{polyorder} = 3
    \end{aligned}
    """
)

# ──────────────────────────────
st.write(r"\- Suppression des valeurs aberrantes des angles (pour $a_n$ et $a_v$) :")

st.latex(
    r"d\theta[i] > 0.135~\mathrm{rad} \;\Rightarrow\; d\theta[i] = d\theta[i-1]"
)

st.latex(
    r"d\theta_z[i] > 0.135~\mathrm{rad} \;\Rightarrow\; d\theta_z[i] = d\theta_z[i-1]"
)

# ──────────────────────────────
st.write(r"\- Suppression des valeurs aberrantes des accélérations :")

st.latex(
    r"a_t[i] > 22.5 \;\Rightarrow\; a_t[i] = a_t[i-1]"
)

st.latex(
    r"\lvert a_n[i] \rvert > 90 \;\Rightarrow\; a_n[i] = a_n[i-1]"
)

st.latex(
    r"\lvert a_v[i] \rvert > 120 \;\Rightarrow\; a_v[i] = a_v[i-1]"
)
