# Checklist de dépôt — Livrable 2 (mercredi 18/11, avant 17h)

Responsable du dépôt : **Alexis**. Objectif : tout est vérifié et déposé **avant 16h30** (30 min de marge).

---

## 1. Qui fait quoi mercredi

| Heure limite | Qui | Tâche | Terminé quand… |
|---|---|---|---|
| 12h | Alexis | Faire tourner l'agent sur l'ancien CRM de Maxime (1 fiche, puis 5) | Le résultat est connu, même partiel |
| 13h | Maxime | Mettre à jour [roadmap.md](roadmap.md) avec l'avancement réel du mercredi | PR fusionnée |
| 13h | Inès | Mettre à jour le tableau « Les briques » de l'[architecture](../architecture/README.md) | PR fusionnée |
| 14h | Inès | Mettre à jour le passage `[…]` du [script du Loom](script-loom.md), **uniquement avec ce qui marche vraiment** | Script relu |
| 15h | Inès | **Enregistrer le Loom** (2 min max), le partager « toute personne ayant le lien » | Lien envoyé à Alexis |
| 15h30 | Alexis | Coller le lien Loom dans le [README du livrable](README.md), cocher la conformité | PR fusionnée |
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
- [ ] Loom : le lien s'ouvre **sans compte Loom** et la vidéo dure **2 min maximum**
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
3. Mini pitch (Loom, 2 min) :
<LIEN LOOM>
4. Roadmap jusqu'à jeudi :
https://github.com/saponealexis1-netizen/Projet_hackathon/blob/main/docs/checkpoint-2/roadmap.md

Prototype en ligne :
• Ancien CRM simulé : https://projet-hackathon-uffi.vercel.app
• Écran de suivi de migration : https://projet-hackathon-jow2.vercel.app
```

## 5. Plans B

| Problème | Que faire |
|---|---|
| Le Loom n'est pas prêt à 15h | Alexis ou Maxime l'enregistre avec le même script ; à 16h30, déposer quand même avec le lien dès qu'il existe |
| L'agent ne lit pas encore l'ancien CRM | Le dire honnêtement dans le Loom : « l'agent a été testé sur une page publique, le branchement sur l'ancien CRM est en cours » |
| Un lien ne s'ouvre pas en navigation privée | Vérifier que le dépôt GitHub est **public** (*Settings → General → Danger Zone*) et que le Loom est partagé « toute personne ayant le lien » |
| Vercel affiche une erreur | Ouvrir le projet dans Vercel → *Deployments* → *Redeploy* sur le dernier déploiement « Ready » |
