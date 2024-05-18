import logo from "@/assets/pyrometric-logo.png";
import { cn } from "@/lib/utils";

export function AppLogo({ className, ...props }) {
  return (
    <img
      src={logo}
      alt="Pyrometric Logo"
      className={cn("h-8 w-8 scale-[2] overflow-hidden", className)}
      {...props}
    />
  );
}
