"""Instructions données à l'agent H et format de réponse imposé.

Propriétaire des règles : Inès (CAIO), reprises de agent/prompts/extraction-v0.md.
Version « zéro configuration » (décision D12) : l'agent ne reçoit QUE l'adresse de l'ancien CRM
et l'identifiant de la fiche. Il ne connaît ni les libellés ni les boutons : il les découvre.
"""

FIELDS = ["legacy_id", "first_name", "last_name", "email", "phone",
          "company", "job_title", "city", "notes"]

# Format JSON imposé à la réponse de l'agent (agent.answer_format) :
# les 9 champs du contrat commun + un champ « error » si la fiche est introuvable.
ANSWER_FORMAT = {
    "type": "object",
    "properties": {
        **{f: {"type": ["string", "null"]} for f in FIELDS},
        "error": {"type": ["string", "null"]},
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
- Les libellés peuvent varier (« Société », « Raison sociale » ou « Entreprise » veulent dire
  la même chose) : fie-toi au sens, pas au mot exact.

CHAMPS À RENVOYER
legacy_id (identifiant), first_name (prénom), last_name (nom), email, phone (téléphone),
company (entreprise), job_title (poste, fonction), city (ville), notes (commentaires, notes).

RÈGLES STRICTES
- Recopie chaque valeur EXACTEMENT comme elle est affichée : ne corrige rien, ne reformate rien.
- N'invente rien. Champ vide, absent ou illisible : null.
- Lecture seule : ne clique jamais sur Enregistrer, Modifier ou Supprimer.
- Si la fiche est introuvable, mets les champs à null et explique le problème dans « error ».
  Sinon, « error » vaut null.
"""

REREAD_FIELD = """Tu vérifies une information dans un ancien logiciel CRM (lecture seule).

Ouvre {url}, trouve la fiche du contact {legacy_id} et relis attentivement le champ
« {field_label} ». Une première lecture a donné : « {previous} », ce qui semble incorrect
({reason}). Il est peut-être caché derrière un onglet ou un bouton « afficher » : ouvre-le.

Renvoie la fiche complète (mêmes règles : recopier exactement, null si absent, ne rien modifier).
"""

FIELD_LABELS = {"email": "e-mail", "phone": "téléphone", "first_name": "prénom",
                "last_name": "nom", "company": "entreprise", "job_title": "poste",
                "city": "ville", "notes": "notes", "legacy_id": "identifiant"}
