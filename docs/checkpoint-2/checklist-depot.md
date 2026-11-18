# Checklist de dépôt — Livrable 2 (mercredi 18/11, avant 17h)

Responsable du dépôt : **Alexis**. Objectif : tout est vérifié et déposé **avant 16h30** (30 min de marge).

---

## 1. Qui fait quoi mercredi

| Heure limite | Qui | Tâche | Terminé quand… |
|---|---|---|---|
| 12h | Alexis | Faire tourner l'agent sur l'ancien CRM de Maxime (1 fiche, puis 5) | Le résultat est connu, même partiel |
| 13h | Maxime | Mettre à jour [roadmap.md](roadmap.md) avec l'avancement réel du mercredi | PR fusionnée |
| 13h | Inès | Mettre à jour le tableau « Les briques » de l'[architecture](../architecture/README.md) | PR fusionnée |
| — | Inès | ✅ Vidéo du mini-pitch : [bascule-avancement.mp4](bascule-avancement.mp4), 2 min, tournée sur le vrai prototype le 18/11 (remplace la vidéo de mardi) | Fait |
| 15h30 | Alexis | Cocher la conformité dans le [README du livrable](README.md) | PR fusionnée |
| 16h | Alexis | **Vérifier tous les liens en navigation privée** (section 3) | Tout s'ouvre |
| **16h30** | **Alexis** | **Déposer le livrable** (section 4) | Dépôt confirmé |

## 2. Ce que le Loom doit dire sur l'avancement (à adapter mercredi)

Ne dire **que ce qui a été vu marcher**. Points déjà vrais au mardi soir :

- ✅ Vérification des fiches et écran de suivi en ligne
- ✅ Envoi dans HubSpot testé (5 contacts envoyés, sans doublon à la relance)
- ✅ Base de l'ancien CRM : 100 contacts fictifs dans Supabase
- ✅ Agent H testé : une fiche lue à 100 %, en 12 s, pour moins d'un centime
- ⏳ À confirmer mercredi : l'ancien CRM de Maxime en ligne, l'agent qui le lit, le parcours complet sur 5 fiches

## 3. Vérification des liens (fenêtre de navigation privée)

Ouvrir chaque lien **sans être connecté** (Chrome : Ctrl+Maj+N). Tout doit s'afficher.

- [ ] Dossier du livrable : https://github.com/saponealexis1-netizen/Projet_hackathon/tree/main/docs/checkpoint-2
- [ ] Parcours utilisateur : https://github.com/saponealexis1-netizen/Projet_hackathon/blob/main/docs/parcours/parcours-utilisateur.md (le schéma Mermaid s'affiche)
- [ ] Architecture : https://github.com/saponealexis1-netizen/Projet_hackathon/blob/main/docs/architecture/README.md (l'image s'affiche en haut)
- [ ] Roadmap : https://github.com/saponealexis1-netizen/Projet_hackathon/blob/main/docs/checkpoint-2/roadmap.md
- [ ] Vidéo : https://github.com/saponealexis1-netizen/Projet_hackathon/raw/main/docs/checkpoint-2/bascule-avancement.mp4 se télécharge sans compte (2 min)
- [ ] Ancien CRM : https://projet-hackathon-uffi.vercel.app
- [ ] Écran de suivi : https://projet-hackathon-jow2.vercel.app (le bouton « Lancer la migration » fonctionne)

Et dans le dépôt :

- [ ] Le [README du livrable](README.md) n'a plus de `⏳` dans « Conformité aux attentes Eugenia »
- [ ] Aucune pull request en attente qui concerne le livrable (onglet *Pull requests*)
- [ ] Aucune clé, aucun mot de passe dans les fichiers (rappel : jamais l'adresse ni le mot de passe du compte d'équipe Eugenia)

## 4. Message de dépôt (à copier)

```
Team 8 — Bascule — Livrable 2 : point intermédiaire

📁 Dossier complet :
https://github.com/saponealexis1-netizen/Projet_hackathon/tree/main/docs/checkpoint-2

1. Parcours utilisateur :
https://github.com/saponealexis1-netizen/Projet_hackathon/blob/main/docs/parcours/parcours-utilisateur.md
2. Architecture technique :
https://github.com/saponealexis1-netizen/Projet_hackathon/blob/main/docs/architecture/README.md
3. Mini pitch (vidéo, 2 min — le lien la télécharge) :
https://github.com/saponealexis1-netizen/Projet_hackathon/raw/main/docs/checkpoint-2/bascule-avancement.mp4
4. Roadmap jusqu'à jeudi :
https://github.com/saponealexis1-netizen/Projet_hackathon/blob/main/docs/checkpoint-2/roadmap.md

Prototype en ligne :
• Ancien CRM simulé : https://projet-hackathon-uffi.vercel.app
• Écran de suivi de migration : https://projet-hackathon-jow2.vercel.app
```

## 5. Plans B

| Problème | Que faire |
|---|---|
| La vidéo ne se lit pas directement sur GitHub | Donner le lien de téléchargement direct : https://github.com/saponealexis1-netizen/Projet_hackathon/raw/main/docs/checkpoint-2/bascule-avancement.mp4 |
| L'agent ne lit pas encore l'ancien CRM | Le dire honnêtement dans le Loom : « l'agent a été testé sur une page publique, le branchement sur l'ancien CRM est en cours » |
| Un lien ne s'ouvre pas en navigation privée | Vérifier que le dépôt GitHub est **public** (*Settings → General → Danger Zone*) et que le Loom est partagé « toute personne ayant le lien » |
| Vercel affiche une erreur | Ouvrir le projet dans Vercel → *Deployments* → *Redeploy* sur le dernier déploiement « Ready » |
