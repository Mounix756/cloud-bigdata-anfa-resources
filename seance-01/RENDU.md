# Rendu Séance 1

**Nom et prénom :** *BLAISE Mouné Tchoubou*  
**Identifiant GitHub :** *Mounix756*  
**Branche :** `seance-01`

---

## Résumé de la séance

Cette première séance avait pour objectif de poser la première brique du projet Anfa : un stockage objet local avec MinIO, alimenté par un script Python via l'API compatible S3. Nous avons également exploré les fondamentaux du cloud computing (modèles de service, de déploiement, caractéristiques NIST) à travers des exercices d'application.

---

## Étapes principales

1. **Installation et vérification de Docker** — vérification que `docker --version` et `docker compose version` répondent correctement (Docker ≥ 24, Compose ≥ 2.20).
2. **Fork du dépôt** — fork de `cloud-bigdata-anfa-resources` sur le compte GitHub personnel, puis clonage local.
3. **Création de la branche de travail** — `git checkout -b seance-01`, puis création du dossier `seance-01/`.
4. **Lancement de MinIO** — téléchargement de l'image `minio/minio` et démarrage du conteneur `anfa-minio` avec exposition des ports 9000 (API S3) et 9001 (console web).
5. **Administration MinIO via `mc`** — connexion au conteneur, configuration de l'alias `local`, création du bucket `anfa-raw`, génération de la paire de clés applicatives `anfa-app-key` / `anfa-app-secret-2026`.
6. **Écriture et exécution du script Python** — création de l'environnement virtuel, installation de `boto3`, écriture de `upload_referentiel.py`, et upload des 4 fichiers CSV du référentiel Anfa.
7. **Vérification visuelle** — consultation de la console MinIO pour confirmer la présence des 4 CSV sous le préfixe `referentiel/`.
8. **Rédaction du `docker-compose.yml`** — création du fichier équivalent à la commande `docker run`, versionnable et lisible.
9. **Commit et push** — envoi de la branche `seance-01` vers le fork GitHub.

---

## Capture d'écran

![Bucket anfa-raw avec les 4 CSV dans la console MinIO](captures/bucket-anfa-raw.png)

*La capture montre les quatre fichiers CSV (`arrets.csv`, `bus.csv`, `lignes.csv`, `tarifs.csv`) visibles dans le bucket `anfa-raw` sous le préfixe `referentiel/`, depuis la console web MinIO accessible sur `http://localhost:9001`.*

---

## Difficultés rencontrées

*Aucune*

---

## Exercices d'application

---

### Exercice 1 : QCM conceptuel

#### 1.1 — Caractéristique non essentielle du cloud selon le NIST

**Réponse : D. Open source obligatoire**

**Justification :** Le NIST définit cinq caractéristiques essentielles du cloud (libre-service à la demande, accès réseau large bande, mutualisation des ressources, élasticité rapide, service mesuré) ; l'open source n'en fait pas partie — un fournisseur peut proposer des services cloud entièrement propriétaires.

---

#### 1.2 — Modèle de service de Gmail

**Réponse : C. SaaS**

**Justification :** Gmail est une application complète accessible via le navigateur, sans aucune installation ni gestion d'infrastructure ou de plateforme de la part de l'utilisateur, ce qui correspond exactement au modèle Software as a Service.

---

#### 1.3 — Modèle pour déclencher une vérification GPS à chaque arrivée de position

**Réponse : D. FaaS**

**Justification :** Le Function as a Service (ex. AWS Lambda, Google Cloud Functions) permet d'exécuter une fonction à la demande en réponse à un événement (ici, l'arrivée d'une position GPS) en quelques millisecondes, sans serveur dédié tournant en permanence, ce qui répond exactement au besoin décrit.

---

#### 1.4 — Modèle de déploiement pour une banque togolaise

**Réponse : C. Cloud hybride**

**Justification :** Le cloud hybride permet de conserver les données sensibles soumises à réglementation dans un cloud privé ou on-premise, tout en profitant de l'élasticité du cloud public pour les traitements analytiques non sensibles.

---

#### 1.5 — Définition du vendor lock-in

**Réponse : B. La situation où une entreprise ne peut plus changer de fournisseur sans coûts ou risques majeurs**

**Justification :** Le vendor lock-in désigne la dépendance technologique, contractuelle ou économique qui rend difficile ou coûteux le changement de fournisseur cloud (APIs propriétaires, formats de données non portables, coûts de migration élevés, etc.).

---

#### 1.6 — Affirmation fausse sur l'open source et le cloud

**Réponse : C. Un service open source est forcément moins performant qu'un service managé propriétaire**

**Justification :** Cette affirmation est fausse : de nombreux services managés des grands clouds (Amazon RDS, Google Dataproc, Azure HDInsight) reposent eux-mêmes sur des briques open source (PostgreSQL, Hadoop, Kafka), et les performances dépendent de l'architecture et de l'optimisation, non du caractère open source ou propriétaire.

---

### Exercice 2 : Classification de services

| Service | Modèle | Justification |
|---|---|---|
| Google Compute Engine (machine virtuelle) | **IaaS** | Fournit des machines virtuelles brutes sur lesquelles l'utilisateur installe et gère lui-même son OS, ses middlewares et ses applications. |
| AWS Lambda | **FaaS** | Exécute des fonctions à la demande en réponse à des événements, sans aucun serveur à provisionner ou gérer. |
| Snowflake (entrepôt de données) | **SaaS** | Entrepôt de données entièrement géré et accessible via une interface web ou des connecteurs SQL, sans infrastructure à administrer. |
| Heroku | **PaaS** | Plateforme qui prend en charge le déploiement, la mise à l'échelle et la gestion des applications ; le développeur pousse uniquement son code. |
| Microsoft 365 (Word, Excel en ligne) | **SaaS** | Suite bureautique complète consommée directement via le navigateur, sans installation ni gestion de plateforme. |
| Databricks (Spark managé) | **PaaS** | Plateforme qui fournit un environnement Spark managé avec notebooks et orchestration ; l'utilisateur se concentre sur ses traitements, pas sur les clusters. |
| Microsoft Azure Functions | **FaaS** | Exécution de fonctions à la demande déclenchées par des événements (HTTP, file de messages, timer…), sans serveur dédié permanent. |
| Tableau Online | **SaaS** | Outil de visualisation de données hébergé et géré par Tableau/Salesforce, accessible via navigateur sans aucune installation locale. |

---

### Exercice 3 : Lecture et interprétation

#### 3.1 — Commande `docker run`

```bash
docker run -d --name analyse-anfa -p 8888:8888 -v /home/koffi/notebooks:/notebooks \
-e JUPYTER_TOKEN=anfa-token \
jupyter/pyspark-notebook
```

| Option | Ce qu'elle fait |
|---|---|
| `-d` | Lance le conteneur en arrière-plan (mode « detached ») : le terminal reste libre et le conteneur continue de tourner. |
| `--name analyse-anfa` | Donne le nom `analyse-anfa` au conteneur, ce qui permet de le désigner par ce nom dans les commandes suivantes (`docker stop analyse-anfa`, etc.) plutôt que par son ID aléatoire. |
| `-p 8888:8888` | Redirige le port 8888 de la machine hôte vers le port 8888 du conteneur, rendant Jupyter accessible depuis le navigateur à `http://localhost:8888`. |
| `-v /home/koffi/notebooks:/notebooks` | Monte le dossier `/home/koffi/notebooks` de la machine hôte dans le conteneur à l'emplacement `/notebooks` : les notebooks créés dans le conteneur sont persistés sur l'hôte (et vice-versa). |
| `-e JUPYTER_TOKEN=anfa-token` | Définit la variable d'environnement `JUPYTER_TOKEN` à la valeur `anfa-token`, qui servira de mot de passe pour accéder à l'interface Jupyter. |
| `jupyter/pyspark-notebook` | Spécifie l'image Docker à utiliser : une image officielle Jupyter qui inclut PySpark, permettant d'exécuter des notebooks avec Apache Spark intégré. |

**Ce que fait la commande entière :** Elle lance en arrière-plan un serveur Jupyter Notebook avec PySpark préinstallé, protégé par le token `anfa-token`, accessible sur `http://localhost:8888`, et dont les notebooks sont sauvegardés sur le disque local de l'utilisateur `koffi` (le dossier local est monté dans le conteneur).

---

#### 3.2 — Lecture du `docker-compose.yml`

```yaml
services:
  minio:
    image: minio/minio:latest
    container_name: anfa-minio
    restart: always
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: anfa-admin
      MINIO_ROOT_PASSWORD: secret
    volumes:
      - minio-data:/data
    command: server /data --console-address ":9001"

volumes:
  minio-data:
```

**a. URLs accessibles depuis le navigateur de l'hôte :**

- `http://localhost:9000` — l'API S3 de MinIO (utilisée par les programmes, les SDK boto3, mc…)
- `http://localhost:9001` — la console web d'administration de MinIO (interface graphique)

**b. Que se passe-t-il si on supprime le conteneur puis qu'on relance `docker compose up -d` ?**

Les données ne sont **pas perdues**. Le conteneur `anfa-minio` est une unité d'exécution éphémère, mais les données sont stockées dans le volume nommé `minio-data`, qui est géré indépendamment par Docker. Lorsqu'on supprime le conteneur avec `docker rm`, le volume `minio-data` subsiste sur l'hôte. Au prochain `docker compose up -d`, un nouveau conteneur est créé et remonte ce même volume : les objets déposés dans MinIO sont donc toujours là.

**c. Problème de sécurité à corriger pour la production :**

Le mot de passe root `MINIO_ROOT_PASSWORD: secret` est écrit **en clair dans le fichier YAML**, qui est généralement versionné dans Git. En production, il faudrait externaliser les secrets via un gestionnaire de secrets (HashiCorp Vault, Docker Secrets, variables d'environnement injectées par CI/CD) et ne jamais committer d'identifiants dans le code source.

---

### Exercice 4 : Diagnostic

**Code de l'étudiant :**
```python
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="anfa-admin",
    aws_secret_access_key="anfa-password-2026",
    ...
)
```

**a. Cause précise de l'erreur :**

L'étudiant utilise `anfa-admin` comme `access_key_id` et `anfa-password-2026` comme `secret_access_key`. Or, `anfa-admin` est le **nom d'utilisateur root** de MinIO (défini via `MINIO_ROOT_USER`), non une **access key S3**. L'API S3 de MinIO (port 9000) attend une paire `access_key` / `secret_key` applicative — c'est-à-dire les clés créées via `mc admin user svcacct add` (partie 3.4 du TP), soit `anfa-app-key` / `anfa-app-secret-2026`. MinIO ne reconnaît pas `anfa-admin` comme identifiant S3 valide, d'où l'erreur `InvalidAccessKeyId`.

**b. Correction du code :**

```python
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="anfa-app-key",          # clé applicative créée via mc
    aws_secret_access_key="anfa-app-secret-2026",  # secret applicatif
    region_name="us-east-1",
)
```

**c. Pourquoi MinIO refuse `anfa-admin` sur l'API S3 mais l'accepte sur la console web ?**

La **console web** (port 9001) est l'interface d'administration de MinIO : elle accepte les identifiants root (`MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`) parce qu'elle gère l'ensemble du serveur.

L'**API S3** (port 9000) est une API de stockage objet qui suit le protocole AWS S3 : elle attend des paires `access_key` / `secret_key` qui sont des identifiants programmatiques distincts, créés spécifiquement pour les applications (service accounts). Ces deux systèmes d'authentification coexistent dans MinIO mais sont séparés : les credentials root ne sont pas des access keys S3 valides.

---

### Exercice 5 : Mini-cas d'architecture (PME togolaise e-commerce alimentaire)

#### a. Deux limites concrètes de l'architecture actuelle

1. **Pas de temps réel :** L'export CSV est mensuel — l'intervalle entre la collecte et la prédiction est donc d'un mois minimum, ce qui rend impossible toute prédiction à l'heure ou même à la journée exigée par la direction.
2. **Pas de partage ni de scalabilité :** Le PC du data scientist est un point de défaillance unique et non partageable — les autres analystes n'ont pas accès aux données et aux modèles, et la capacité de calcul est fixe et limitée à la machine physique, sans possibilité d'absorber les pics de demande (vendredi soir, fêtes).

---

#### b. Besoins de la direction ↔ caractéristiques NIST

| Besoin | Caractéristique NIST | Explication |
|---|---|---|
| Prédictions en quasi temps réel (chaque heure) | **Service mesuré (pay-as-you-go)** | Les ressources de calcul sont consommées et facturées uniquement pendant l'heure de calcul, ce qui rend économiquement viable un traitement récurrent toutes les heures. |
| Tableau de bord partagé, sans installation locale | **Libre-service à la demande** | Les analystes accèdent à l'outil depuis leur navigateur à tout moment, sans demander une intervention informatique préalable ni installer quoi que ce soit. |
| Augmenter la capacité lors des pics | **Élasticité rapide** | Le cloud peut allouer automatiquement des ressources supplémentaires en quelques minutes lors des pics (vendredi soir, fêtes) et les libérer ensuite. |
| Maîtriser les coûts et pouvoir changer de fournisseur | **Mutualisation des ressources** | Les ressources partagées entre de nombreux clients réduisent les coûts unitaires ; en utilisant des standards ouverts (API S3, containers), la PME conserve la portabilité inter-fournisseurs. |
| Données clients dans un environnement contrôlé | **Mutualisation des ressources** *(cloud privé)* | Un cloud privé ou un segment dédié permet de contrôler l'emplacement et l'accès aux données clients tout en conservant les bénéfices du cloud. |

---

#### c. Modèles de service pour chaque composant

**(i) Tableau de bord partagé → SaaS**  
Un outil de visualisation SaaS (ex. Metabase Cloud, Looker, Power BI en ligne) est accessible depuis n'importe quel navigateur sans installation, géré et maintenu par le fournisseur. C'est le modèle le plus adapté pour un partage immédiat entre analystes.

**(ii) Calcul des prédictions à l'heure → FaaS ou PaaS**  
Le FaaS (ex. AWS Lambda, Google Cloud Functions) est idéal si le modèle de prédiction est léger : une fonction est déclenchée toutes les heures par un planificateur (cron), s'exécute et s'arrête. Si le modèle est plus lourd (Spark, MLflow), un PaaS managé (ex. Databricks, Vertex AI) est plus adapté.

**(iii) Stockage des données clients → IaaS ou cloud privé managé**  
Pour respecter la contrainte de conformité, les données clients doivent rester dans un environnement contrôlé. Un stockage sur IaaS dans une région géographique maîtrisée (ou un cloud privé on-premise) avec chiffrement et contrôle d'accès fin est recommandé.

---

#### d. Modèle de déploiement recommandé

**Cloud hybride.**

Les données clients sensibles (soumises à conformité réglementaire) sont conservées dans un cloud privé ou on-premise, garantissant le contrôle total sur leur localisation et leur accès. En parallèle, les charges de travail non sensibles (entraînement de modèles, tableaux de bord, calcul des prédictions) sont hébergées dans un cloud public, ce qui permet de bénéficier de l'élasticité lors des pics (vendredi soir, fêtes) et de ne payer que ce qui est consommé. Les deux environnements communiquent via des API sécurisées.

---

#### e. Trois stratégies pour limiter le vendor lock-in

1. **Utiliser des standards et outils open source** : privilégier des formats de données ouverts (Parquet, CSV, Delta Lake), des APIs standardisées (protocole S3 pour le stockage objet, JDBC/ODBC pour les bases de données) et des outils portables (MinIO, Kafka, Spark) qui fonctionnent chez n'importe quel fournisseur cloud.

2. **Conteneuriser les applications** : empaqueter les modèles et pipelines dans des images Docker déployables sur tout environnement Kubernetes (EKS, GKE, AKS, ou on-premise) — le code n'est plus lié à un service propriétaire spécifique.

3. **Adopter une stratégie multi-cloud ou d'abstraction** : utiliser une couche d'abstraction (ex. Terraform pour l'infrastructure, un orchestrateur neutre comme Airflow pour les pipelines) et tester régulièrement la migration d'une charge de travail vers un autre fournisseur, afin que le coût et le risque de changement restent maîtrisés.
