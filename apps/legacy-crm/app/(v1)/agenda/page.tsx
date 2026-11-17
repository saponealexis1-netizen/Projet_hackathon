import Link from "next/link";
import { connection } from "next/server";
import { getContacts, type Contact } from "@/lib/contacts";

type Props = {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
};

const MONTHS = [
  "janvier", "février", "mars", "avril", "mai", "juin",
  "juillet", "août", "septembre", "octobre", "novembre", "décembre",
];
const DAYS = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"];
const KINDS = ["RDV", "Appel", "Relance devis", "RDV", "Appel"];
const HOURS = ["09:00", "10:30", "11:15", "14:00", "15:30", "16:45"];

type Appointment = { time: string; kind: string; contact: Contact };

/**
 * Faux rendez-vous, toujours identiques pour un mois donné (pas de hasard),
 * reliés aux contacts de la base : un clic ouvre la fiche du contact.
 */
function fakeAppointments(year: number, month: number, contacts: Contact[]) {
  const byDay = new Map<number, Appointment[]>();
  if (contacts.length === 0) return byDay;
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  for (let day = 1; day <= daysInMonth; day++) {
    const weekday = new Date(year, month, day).getDay(); // 0 = dimanche
    if (weekday === 0 || weekday === 6) continue;
    const seed = (year * 372 + month * 31 + day) * 7;
    const count = seed % 3; // 0, 1 ou 2 rendez-vous
    const list: Appointment[] = [];
    for (let i = 0; i < count; i++) {
      list.push({
        time: HOURS[(seed + i * 2) % HOURS.length],
        kind: KINDS[(seed + i) % KINDS.length],
        contact: contacts[(seed + i * 5) % contacts.length],
      });
    }
    list.sort((a, b) => a.time.localeCompare(b.time));
    if (list.length) byDay.set(day, list);
  }
  return byDay;
}

export default async function AgendaPage({ searchParams }: Props) {
  await connection();

  const today = new Date();
  const raw = (await searchParams).mois;
  const match = typeof raw === "string" ? /^(\d{4})-(\d{2})$/.exec(raw) : null;
  const year = match ? Number(match[1]) : today.getFullYear();
  const month = match && Number(match[2]) >= 1 && Number(match[2]) <= 12 ? Number(match[2]) - 1 : today.getMonth();

  const contacts = await getContacts();
  const appointments = fakeAppointments(year, month, contacts);

  const firstWeekday = (new Date(year, month, 1).getDay() + 6) % 7; // lundi = 0
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const cells: (number | null)[] = [
    ...Array<null>(firstWeekday).fill(null),
    ...Array.from({ length: daysInMonth }, (_, i) => i + 1),
  ];
  while (cells.length % 7) cells.push(null);

  const key = (y: number, m: number) => `${y}-${String(m + 1).padStart(2, "0")}`;
  const prev = month === 0 ? key(year - 1, 11) : key(year, month - 1);
  const next = month === 11 ? key(year + 1, 0) : key(year, month + 1);
  const isToday = (d: number) =>
    d === today.getDate() && month === today.getMonth() && year === today.getFullYear();

  return (
    <>
      <h1>Agenda</h1>

      <div className="toolbar">
        <Link className="button" href={`/agenda?mois=${prev}`}>
          ◄ Mois précédent
        </Link>
        <b style={{ minWidth: 140, textAlign: "center" }}>
          {MONTHS[month]} {year}
        </b>
        <Link className="button" href={`/agenda?mois=${next}`}>
          Mois suivant ►
        </Link>
        <Link className="button" href="/agenda">
          Aujourd&apos;hui
        </Link>
      </div>

      <table className="calendar">
        <thead>
          <tr>
            {DAYS.map((d) => (
              <th key={d} scope="col">
                {d}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: cells.length / 7 }, (_, w) => (
            <tr key={w}>
              {cells.slice(w * 7, w * 7 + 7).map((day, i) => (
                <td key={i} className={day === null ? "calendar-empty" : isToday(day) ? "calendar-today" : undefined}>
                  {day !== null && (
                    <>
                      <div className="calendar-day">{day}</div>
                      {appointments.get(day)?.map((a) => (
                        <Link
                          key={a.time + a.contact.legacy_id}
                          className="calendar-event"
                          href={`/contacts/${a.contact.legacy_id}`}
                        >
                          {a.time} {a.kind} — {a.contact.last_name}
                        </Link>
                      ))}
                    </>
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}
