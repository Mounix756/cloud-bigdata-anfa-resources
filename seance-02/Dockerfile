# ──────────────────────────────────────────────────────────────
# Dockerfile pour l'application d'analyse du référentiel Anfa
# ──────────────────────────────────────────────────────────────
# Dockerfile pour l'application d'analyse du référentiel Anfa
# ──────────────────────────────────────────────────────────────

# FROM : image de base. On part de Python 3.12 minimal (Debian slim).
# Le tag "3.12-slim" garantit la reproductibilité (vs "latest" qui change).
FROM python:3.11-slim-bookworm

# ENV : variables d'environnement persistantes dans l'image.
# PYTHONDONTWRITEBYTECODE : pas de fichiers .pyc dans le conteneur.
# PYTHONUNBUFFERED : flush immédiat des prints (utile pour les logs).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Spark a besoin de Java pour fonctionner (Spark est en Scala/JVM).
# On installe le JRE 17 (Java Runtime Environment) en version "headless"
# (sans interface graphique). On nettoie le cache apt dans la MÊME
# couche pour éviter de l'embarquer dans l'image finale.
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jre-headless && \
    rm -rf /var/lib/apt/lists/*

# Variable d'environnement requise par Spark pour trouver Java.
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# WORKDIR : dossier de travail dans le conteneur (équivalent d'un "cd").
# S'il n'existe pas, Docker le crée.
WORKDIR /app


# Copie SEULEMENT requirements.txt en premier, puis installe les deps.
# Pourquoi ? Tant que requirements.txt ne change pas, Docker réutilise
# le cache de cette couche → pip install n'est pas relancé à chaque
# modification du code. (Voir partie 2.)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code applicatif (le script Python).
# Cette couche change souvent ; elle est volontairement placée
# APRÈS l'installation des dépendances.
COPY . .


# CMD : commande exécutée au démarrage du conteneur.
# Format "exec" (liste) : recommandé, plus prévisible que la forme shell.
CMD ["python", "analyse_referentiel.py"]