import "./globals.css";

/** Racine commune aux deux versions de l'ancien CRM (v1 « 2010 » et /v2). */
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
