function LanguageChip({ language }) {
  return <li className="rounded-md bg-gray-200 text-gray-800">{language}</li>;
}

export function LanguageList({ languages }) {
  return (
    <ul className="flex flex-wrap gap-2">
      {languages.map((language) => (
        <LanguageChip key={language} language={language} />
      ))}
    </ul>
  );
}
