import { cn } from "@/lib/utils";
import { CircularProgress } from "./circular-progress";

export function ScoreIndicator({ percentage }) {
  const textSizeClass = percentage < 100 ? "text-lg" : "text-md";

  return (
    <div className="relative h-[50px] w-[50px]">
      <CircularProgress width={50} height={50} progress={percentage} />
      <div className="absolute left-0 top-0 flex h-full w-full items-center justify-center">
        <p className={cn("font-semibold", textSizeClass)}>{percentage}</p>
      </div>
    </div>
  );
}
