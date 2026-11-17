import { connection } from "next/server";
import OptionsForm from "@/components/OptionsForm";
import { getContacts } from "@/lib/contacts";

export default async function ToolsPage() {
  await connection();
  const contacts = await getContacts();

  const info: [string, string][] = [
    ["Nombre de fiches", String(contacts.length)],
    ["Version du logiciel", "3.1 (build 2010.03)"],
    ["Installation", "12/03/2010"],
    ["Type de licence", "Consultation (lecture seule)"],
    ["Fin du support éditeur", "31/12/2015"],
  ];

  return (
    <>
      <h1>Options</h1>
      <OptionsForm />

      <fieldset id="base">
        <legend>Informations sur la base</legend>
        <table className="form">
          <tbody>
            {info.map(([label, value]) => (
              <tr key={label}>
                <th scope="row">{label} :</th>
                <td>
                  <span className="field">{value}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </fieldset>
    </>
  );
}
