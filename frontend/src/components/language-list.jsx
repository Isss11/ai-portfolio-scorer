function LanguageChip({ name, color }) {
  return (
    <li className="flex items-center gap-1 text-sm text-muted-foreground">
      <div
        className="h-3 w-3 rounded-full border border-border"
        style={{ background: color }}
      />
      {name}
    </li>
  );
}

export function LanguageList({ languages }) {
  return (
    <ul className="flex flex-wrap gap-3">
      {languages.map((language) => (
        <LanguageChip key={language.name} {...language} />
      ))}
    </ul>
  );
}
