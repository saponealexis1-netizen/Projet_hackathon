"""Instructions données à l'agent H et format de réponse imposé.

Propriétaire des règles : Inès (CAIO), reprises de agent/prompts/extraction-v0.md.
Version « zéro configuration » (décision D12) : l'agent ne reçoit QUE l'adresse de l'ancien CRM
et l'identifiant de la fiche. Il ne connaît ni les libellés ni les boutons : il les découvre.
"""

FIELDS = ["legacy_id", "first_name", "last_name", "email", "phone",
          "company", "job_title", "city", "notes"]

# Format JSON imposé à la réponse de l'agent (agent.answer_format) :
# les 9 champs du contrat commun + un champ « error » si la fiche est introuvable.
# Uniquement des chaînes : plus simple pour l'agent (« texte ou null » le perturbait).
# Chaîne vide = information absente ; la vérification transforme "" en null.
ANSWER_FORMAT = {
    "type": "object",
    "properties": {
        **{f: {"type": "string", "description": f"valeur affichée pour « {f} », ou chaîne vide si absente"}
           for f in FIELDS},
        "error": {"type": "string", "description": "chaîne vide si la fiche a été lue, sinon le problème"},
    },
    "required": FIELDS + ["error"],
    "additionalProperties": False,
}

READ_RECORD = """Tu recopies une fiche client depuis un ancien logiciel CRM qui n'a ni export ni API.
Tu dois lire l'écran, comme un humain.

OBJECTIF
Ouvre {url} et lis la fiche du contact dont l'identifiant (n° client, référence…) est {legacy_id}.

COMMENT FAIRE
- Tu ne connais pas ce logiciel : explore-le. Ferme les fenêtres ou messages qui gênent.
- Trouve la liste des contacts. Si la fiche n'est pas sur la page, passe aux pages suivantes.
- Ouvre la fiche. Certaines informations peuvent être cachées : derrière un onglet, un bouton
  « afficher », « voir plus »… Ouvre-les pour tout lire.
- Vérifie que l'identifiant affiché sur la fiche ouverte est EXACTEMENT {legacy_id}, caractère par
  caractère (C-0070 n'est pas C-0007). Sinon, retourne à la liste et cherche la bonne fiche.
- Les libellés peuvent varier (« Société », « Raison sociale » ou « Entreprise » veulent dire
  la même chose) : fie-toi au sens, pas au mot exact.

CHAMPS À RENVOYER
legacy_id (identifiant), first_name (prénom), last_name (nom), email, phone (téléphone),
company (entreprise), job_title (poste, fonction), city (ville), notes (commentaires, notes).

RÈGLES STRICTES
- Recopie chaque valeur EXACTEMENT comme elle est affichée : ne corrige rien, ne reformate rien.
- Une valeur n'est valable que si tu la VOIS écrite à l'écran. Si un champ affiche un bouton
  (« Afficher », « Voir », « Voir le tél. »…) au lieu d'une valeur, CLIQUE dessus et lis la valeur
  qui apparaît. Ne déduis JAMAIS une valeur d'un motif, d'une autre fiche ou de l'identifiant.
- Avant de répondre, vérifie sur l'écran que chaque valeur renvoyée y est bien visible,
  caractère par caractère (attention aux chiffres des numéros de téléphone).
- Champ vide, absent ou que tu n'as pas pu afficher : chaîne vide "". Mieux vaut vide qu'une valeur inventée.
- Chaque champ contient UNE seule valeur : ne mets jamais toute la fiche dans un champ.
- Lecture seule : ne clique jamais sur Enregistrer, Modifier ou Supprimer.
- Si la fiche est introuvable, laisse les champs vides et explique le problème dans « error ».
  Sinon, « error » est une chaîne vide.
"""

REREAD_FIELD = """Tu vérifies une information dans un ancien logiciel CRM (lecture seule).

Ouvre {url}, trouve la fiche du contact {legacy_id} et relis attentivement le champ
« {field_label} ». Une première lecture a donné : « {previous} », ce qui semble incorrect
({reason}). Il est peut-être caché derrière un onglet ou un bouton « afficher » : ouvre-le.

Renvoie la fiche complète (mêmes règles : recopier exactement, chaîne vide si absent, ne rien modifier).
"""

FIELD_LABELS = {"email": "e-mail", "phone": "téléphone", "first_name": "prénom",
                "last_name": "nom", "company": "entreprise", "job_title": "poste",
                "city": "ville", "notes": "notes", "legacy_id": "identifiant"}
