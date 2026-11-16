# Ancien CRM simulé (`apps/legacy-crm`)

Application Next.js qui joue le rôle du **vieux CRM sans export ni API** que l'agent H Company doit lire à l'écran.
Propriétaire : Victoria (voir [docs/ORGANISATION.md](../../docs/ORGANISATION.md)).

## Lancer en local

```bash
cd apps/legacy-crm
npm install
cp .env.example .env.local   # puis mettre SA clé dans .env.local
npm run dev                  # http://localhost:3000
```

Avant tout commit, vérifier que la clé est bien ignorée :

```bash
git check-ignore -v apps/legacy-crm/.env.local
```

## Déployer sur Vercel

- Importer le dépôt dans Vercel.
- **Root Directory : `apps/legacy-crm`**.
- Variables d'environnement : `H_COMPANY_API_KEY` = la clé de Victoria (voir section 8 de `docs/ORGANISATION.md`).
