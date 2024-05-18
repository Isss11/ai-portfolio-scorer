import { Link } from "react-router-dom";
import { Button } from "./ui/button";
import { AppLogo } from "./logo";

export function Navbar() {
  return (
    <nav>
      <ul className="flex gap-3 p-3">
        <li>
          <Button asChild size="sm" variant="ghost">
            <Link to="/" className="flex gap-1">
              <AppLogo />
              Pyrometric
            </Link>
          </Button>
        </li>
        <li>
          <Button asChild size="sm" variant="link">
            <Link to="/analyze">Analyze</Link>
          </Button>
        </li>
        <li>
          <Button asChild size="sm" variant="link">
            <Link to="/compare">Compare</Link>
          </Button>
        </li>
      </ul>
    </nav>
  );
}
