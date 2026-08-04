# Fiche de conformité — Application mobile passagers Anfa

> Gabarit fourni. Complétez chaque section **en 2-4 lignes**, en vous appuyant sur le CM.
> Il n'y a pas de "bonne réponse" unique sur certains points — l'important est le raisonnement.

## 1. Finalité du traitement
Chaque donnée sert un usage précis et rien d'autre : la position GPS sert à proposer le trajet ou l'arrêt le plus proche du passager, l'historique mobile money sert à gérer son abonnement (facturation, renouvellement), et le numéro de téléphone sert d'identifiant de compte. Le principe de finalité déterminée interdit de réutiliser ces données à d'autres fins non annoncées (ex. revente à des annonceurs, profilage marketing) sans nouveau consentement explicite du passager.

## 2. Données collectées et leur sensibilité
Les 3 données du scénario : position GPS du passager, historique de paiements mobile money, numéro de téléphone. La plus sensible est l'**historique mobile money** : nominative, elle révèle la situation financière et les habitudes de consommation d'un individu. Croisée avec la géolocalisation continue, elle permettrait de reconstituer un profil quasi complet de sa vie quotidienne (domicile, lieu de travail, capacité de paiement, habitudes de déplacement). C'est l'effet de recoupement qui est dangereux, pas chaque donnée isolément.

## 3. Base légale applicable
La loi togolaise n°2019-014 relative à la protection des données à caractère personnel s'applique aux 3 données, puisque toutes identifient une personne physique (consentement, finalité, droits des personnes). L'historique mobile money relève en plus d'un cadre sectoriel spécifique aux transactions électroniques (loi 2017-007, modifiée par la loi 2023-012), qui impose ses propres obligations de traçabilité (lutte anti-blanchiment, KYC), *à vérifier avec précision dans les supports de CM*. Le principe à retenir est que ces deux textes peuvent s'appliquer simultanément à une même donnée : 2019-014 protège la donnée en tant que donnée personnelle, la réglementation sectorielle encadre en plus son usage financier, avec parfois des obligations de conservation plus longues qui priment sur la minimisation pure.

## 4. Durée de conservation
Par principe de minimisation, chaque donnée n'est gardée que le temps nécessaire à sa finalité : la position GPS est volatile et n'a d'utilité que pour la session en cours ou des statistiques agrégées anonymisées à court terme (quelques semaines maximum en donnée brute) ; le numéro de téléphone est conservé tant que le compte est actif, plus une courte période de latence après suppression pour gérer d'éventuels litiges. L'historique mobile money est l'exception : une obligation réglementaire externe (traçabilité financière) peut imposer une conservation plus longue que ce que la seule minimisation justifierait.

## 5. Hébergement et souveraineté
Les données les plus sensibles (mobile money, GPS) devraient être hébergées au Togo ou dans un cloud régional ouest-africain, en cohérence avec la loi 2019-014 et l'esprit de souveraineté numérique porté par la Convention de Malabo. Le risque d'un hébergement chez un cloud américain (AWS, GCP, Azure US) est le **CLOUD Act** : il autorise les autorités américaines à exiger l'accès aux données d'un fournisseur américain même si les serveurs physiques sont hors des États-Unis. Cette extraterritorialité contredit directement la protection voulue par la loi togolaise, quel que soit l'endroit réel où les octets sont stockés.

## 6. Droit des personnes concernées
Oui, un passager doit pouvoir demander la suppression de ses données (droit à l'effacement, consacré par la loi 2019-014 comme par le RGPD). Le système technique actuel d'Anfa, tel que construit depuis la séance 1, ne le permettrait **pas facilement** : les données sont stockées en fichiers plats (CSV/Parquet) dans MinIO, organisées par ligne ou par date, sans identifiant de passager indexé ni mécanisme de suppression ciblée. Retrouver et effacer toutes les traces d'un individu précis nécessiterait de parcourir l'ensemble des fichiers. Il manque une couche d'identité/consentement pensée dès la conception (« droit à l'oubli by design »), avec une clé de suppression et une séparation claire entre données nominatives et données agrégées ou anonymisées.
