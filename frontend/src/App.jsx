import { useEffect, useMemo, useState } from "react";
import {
  AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer,
} from "recharts";

const API = "http://127.0.0.1:8000";

// Fonctions de formatage
const fmtM = (v) => `${(v / 1e6).toLocaleString("fr-FR", { maximumFractionDigits: 1 })} M`;
const fmtNb = (v) => v.toLocaleString("fr-FR");
const fmtDate = (j) =>
  new Date(j).toLocaleDateString("fr-FR", { day: "numeric", month: "short" });
const fmtDateLongue = (j) =>
  new Date(j).toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long" });

const AXE = { fill: "#8b97b1", fontSize: 12 };
const GRILLE = "#26324a";

// Composants réutilisables
function Kpi({ label, value, detail }) {
  return (
    <div className="kpi">
      <div className="label">{label}</div>
      <div className="value">{value}</div>
      <div className="detail">{detail}</div>
    </div>
  );
}

function Card({ titre, sousTitre, children }) {
  return (
    <section className="card">
      <h2>{titre}</h2>
      <p className="sub">{sousTitre}</p>
      {children}
    </section>
  );
}

function ChartTooltip({ active, payload, label, formatLabel }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="tooltip">
      <strong>{formatLabel ? formatLabel(label) : label}</strong>
      {fmtNb(payload[0].value)} validations
    </div>
  );
}

export default function App() {
  const [parJour, setParJour] = useState([]);
  const [topStations, setTopStations] = useState([]);
  const [parTitre, setParTitre] = useState([]);
  const [erreur, setErreur] = useState(null);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/validations/par-jour`).then((r) => r.json()),
      fetch(`${API}/stations/top?limite=10`).then((r) => r.json()),
      fetch(`${API}/validations/par-titre`).then((r) => r.json()),
    ])
      .then(([jours, stations, titres]) => {
        setParJour(jours);
        setTopStations(stations);
        setParTitre(titres);
      })
      .catch(() => setErreur("Impossible de joindre l'API"));
  }, []);

  // Chiffres clés calculés à partir des données
  const stats = useMemo(() => {
    if (!parJour.length) return null;
    const total = parJour.reduce((s, j) => s + j.total, 0);
    const max = parJour.reduce((a, b) => (b.total > a.total ? b : a));
    const min = parJour.reduce((a, b) => (b.total < a.total ? b : a));
    return { total, moyenne: total / parJour.length, max, min };
  }, [parJour]);

  if (erreur) return <div className="container"><p>{erreur}</p></div>;
  if (!stats) return <div className="container"><p>Chargement…</p></div>;

  return (
    <div className="container">
      <header className="header">
        <h1>Fréquentation du réseau ferré IDF</h1>
        <p>Métro, RER et Transilien · 4ème trimestre 2025</p>
      </header>

      <div className="kpis">
        <Kpi label="Validations sur le trimestre" value={fmtM(stats.total)} detail="Total toutes stations" />
        <Kpi label="Moyenne par jour" value={fmtM(stats.moyenne)} detail="Sur 92 jours" />
        <Kpi label="Jour le plus chargé" value={fmtM(stats.max.total)} detail={fmtDateLongue(stats.max.jour)} />
        <Kpi label="Jour le plus calme" value={fmtM(stats.min.total)} detail={fmtDateLongue(stats.min.jour)} />
      </div>

      <Card titre="Validations par jour" sousTitre="Les creux réguliers correspondent aux week-ends">
        <ResponsiveContainer width="100%" height={320}>
          <AreaChart data={parJour}>
            <defs>
              <linearGradient id="degrade" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.5} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke={GRILLE} strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="jour" tickFormatter={fmtDate} tick={AXE} minTickGap={40} axisLine={false} tickLine={false} />
            <YAxis tickFormatter={fmtM} tick={AXE} width={60} axisLine={false} tickLine={false} />
            <Tooltip content={<ChartTooltip formatLabel={fmtDateLongue} />} />
            <Area type="monotone" dataKey="total" stroke="#3b82f6" strokeWidth={2} fill="url(#degrade)" />
          </AreaChart>
        </ResponsiveContainer>
      </Card>

      <div className="grid-2">
        <Card titre="Top 10 des stations" sousTitre="Total des validations sur le trimestre">
          <ResponsiveContainer width="100%" height={380}>
            <BarChart data={topStations} layout="vertical" margin={{ right: 20 }}>
              <CartesianGrid stroke={GRILLE} strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" tickFormatter={fmtM} tick={AXE} axisLine={false} tickLine={false} />
              <YAxis type="category" dataKey="nom_arret" width={105} tick={AXE} axisLine={false} tickLine={false} />
              <Tooltip content={<ChartTooltip />} cursor={{ fill: "rgba(255,255,255,0.05)" }} />
              <Bar dataKey="total" fill="#8b5cf6" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        <Card titre="Type de titre de transport" sousTitre="Le Forfait Navigo domine largement">
          <ResponsiveContainer width="100%" height={380}>
            <BarChart data={parTitre} layout="vertical" margin={{ right: 20 }}>
              <CartesianGrid stroke={GRILLE} strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" tickFormatter={fmtM} tick={AXE} axisLine={false} tickLine={false} />
              <YAxis type="category" dataKey="categorie_titre" width={150} tick={AXE} axisLine={false} tickLine={false} />
              <Tooltip content={<ChartTooltip />} cursor={{ fill: "rgba(255,255,255,0.05)" }} />
              <Bar dataKey="total" fill="#22c55e" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <p className="footer">Source : Île-de-France Mobilités (open data) · Python, SQLite, FastAPI, React</p>
    </div>
  );
}