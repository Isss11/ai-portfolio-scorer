import logo from "@/assets/pyrometric-logo.png";
import { cn } from "@/lib/utils";

export function AppLogo({ className, ...props }) {
  return (
    <img
      src={logo}
      alt="Pyrometric Logo"
      className={cn("h-12 w-12 scale-110 overflow-hidden", className)}
      {...props}
    />
  );
}
