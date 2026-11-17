"use client";

/** Boîte de dialogue « à l'ancienne » (style Windows classique). */
export default function Dialog({
  title,
  icon = "ℹ️",
  children,
  buttons,
}: {
  title: string;
  icon?: string;
  children: React.ReactNode;
  buttons: { label: string; onClick: () => void }[];
}) {
  return (
    <div className="dialog-backdrop" role="presentation">
      <div className="dialog" role="dialog" aria-modal="true" aria-label={title}>
        <div className="titlebar">
          <span>{title}</span>
        </div>
        <div className="dialog-body">
          <span className="dialog-icon" aria-hidden="true">
            {icon}
          </span>
          <div>{children}</div>
        </div>
        <div className="dialog-buttons">
          {buttons.map((b, i) => (
            <button key={b.label} type="button" onClick={b.onClick} autoFocus={i === 0}>
              {b.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
