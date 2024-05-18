import { cn } from "@/lib/utils";

export function PageContainer({ className, ...props }) {
  return (
    <div className={cn("flex min-h-[100dvh] flex-col", className)} {...props} />
  );
}
