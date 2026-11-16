-- Bascule — chargement des 20 contacts d'exemple dans legacy_contacts.
-- Fichier GÉNÉRÉ depuis data/contacts.sample.json par data/generate_seed.py : ne pas modifier à la main.
-- À lancer APRÈS la migration des tables. Peut être relancé sans créer de doublons.

insert into public.legacy_contacts (legacy_id, first_name, last_name, email, phone, company, job_title, city, notes) values
  ('C-0001', 'Julien', 'Moreau', 'julien.moreau@boulangerie-moreau.example', '+33 6 39 98 00 01', 'Boulangerie Moreau', 'Gérant', 'Lyon', 'Commande hebdomadaire de flyers'),
  ('C-0002', 'Sophie', 'Lefèvre', 'sophie.lefevre@cabinet-lefevre-conseil.example', '+33 6 39 98 00 02', 'Cabinet Lefèvre Conseil', 'Associée', 'Paris', 'Rappeler en janvier'),
  ('C-0003', 'Karim', 'Benali', 'karim.benali@transports-benali.example', '+33 6 39 98 00 03', 'Transports Benali', 'Directeur commercial', 'Marseille', null),
  ('C-0004', 'Élodie', 'Garnier', 'elodie.garnier@atelier-garnier.example', '+33 6 39 98 00 04', 'Atelier Garnier', 'Fondatrice', 'Nantes', 'Préfère être contactée par e-mail'),
  ('C-0005', 'Thomas', 'Roux', 'thomas.roux@roux-immobilier.example', '+33 6 39 98 00 05', 'Roux Immobilier', 'Agent immobilier', 'Bordeaux', 'Client depuis 2018'),
  ('C-0006', 'Nadia', 'Haddad', 'nadia.haddad@pharmacie-du-centre.example', '+33 6 39 98 00 06', 'Pharmacie du Centre', 'Pharmacienne titulaire', 'Lille', null),
  ('C-0007', 'Lucas', 'Fontaine', 'lucas.fontaine@fontaine-renovation.example', '+33 6 39 98 00 07', 'Fontaine Rénovation', 'Chef de chantier', 'Toulouse', 'Devis envoyé le 12/09'),
  ('C-0008', 'Chloé', 'Mercier', 'chloe.mercier@studio-mercier.example', '+33 6 39 98 00 08', 'Studio Mercier', 'Photographe', 'Rennes', null),
  ('C-0009', 'Antoine', 'Dubois', 'antoine.dubois@dubois-fils.example', '+33 6 39 98 00 09', 'Dubois & Fils', 'Directeur', 'Strasbourg', 'Ancien client, à relancer'),
  ('C-0010', 'Inès', 'Rahmani', 'ines.rahmani@agence-horizon.example', '+33 6 39 98 00 10', 'Agence Horizon', 'Chargée de communication', 'Montpellier', null),
  ('C-0011', 'Mathieu', 'Perrin', 'mathieu.perrin@perrin-logistique.example', '+33 6 39 98 00 11', 'Perrin Logistique', 'Responsable achats', 'Grenoble', 'Volume important au T4'),
  ('C-0012', 'Laura', 'Chevalier', 'laura.chevalier@chevalier-evenements.example', '+33 6 39 98 00 12', 'Chevalier Événements', 'Gérante', 'Nice', null),
  ('C-0013', 'Hugo', 'Lambert', 'hugo.lambert@garage-lambert.example', '+33 6 39 98 00 13', 'Garage Lambert', 'Mécanicien', 'Dijon', 'Paiement à 30 jours'),
  ('C-0014', 'Sarah', 'Bouvier', 'sarah.bouvier@bouvier-avocats.example', '+33 6 39 98 00 14', 'Bouvier Avocats', 'Avocate', 'Angers', null),
  ('C-0015', 'Mehdi', 'Saïdi', 'mehdi.saidi@saidi-traiteur.example', '+33 6 39 98 00 15', 'Saïdi Traiteur', 'Gérant', 'Reims', 'Salon professionnel en mars'),
  ('C-0016', 'Camille', 'Renard', 'camille.renard@librairie-renard.example', '+33 6 39 98 00 16', 'Librairie Renard', 'Libraire', 'Tours', null),
  ('C-0017', 'Paul', 'Girard', 'paul.girard@girard-informatique.example', '+33 6 39 98 00 17', 'Girard Informatique', 'Technicien', 'Clermont-Ferrand', 'Contrat de maintenance annuel'),
  ('C-0018', 'Manon', 'Blanc', 'manon.blanc@blanc-coiffure.example', '+33 6 39 98 00 18', 'Blanc Coiffure', 'Coiffeuse', 'Le Havre', null),
  ('C-0019', 'Yanis', 'Morel', 'yanis.morel@morel-paysage.example', '+33 6 39 98 00 19', 'Morel Paysage', 'Paysagiste', 'Metz', 'Intéressé par l''offre pro'),
  ('C-0020', 'Claire', 'Vidal', 'claire.vidal@vidal-architecture.example', '+33 6 39 98 00 20', 'Vidal Architecture', 'Architecte', 'Aix-en-Provence', null)
on conflict (legacy_id) do update set
  first_name = excluded.first_name,
  last_name = excluded.last_name,
  email = excluded.email,
  phone = excluded.phone,
  company = excluded.company,
  job_title = excluded.job_title,
  city = excluded.city,
  notes = excluded.notes;
