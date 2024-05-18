import { Flame } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "./ui/button";

export function Navbar() {
  return (
    <nav>
      <ul className="flex gap-3 p-3">
        <li>
          <Button asChild size="sm" variant="ghost">
            <Link to="/" className="flex gap-1">
              <Flame className="text-red-500" /> Pyrometric
            </Link>
          </Button>
        </li>
        <li>
          <Button asChild size="sm" variant="link">
            <Link to="/analyze">Analyze</Link>
          </Button>
        </li>
      </ul>
    </nav>
  );
}
