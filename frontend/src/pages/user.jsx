import { Navbar } from "@/components/navbar";
import { PageContainer } from "@/components/page-container";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { initiateEventSource } from "@/lib/api";
import { useState } from "react";
import { useEffect } from "react";
import { useParams } from "react-router-dom";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { CircularProgress } from "@/components/circular-progress";
import { cn } from "@/lib/utils";

function ScoreIndicator({ percentage }) {
  const textSizeClass = percentage < 100 ? "text-xl" : "text-lg";
  return (
    <div className="relative">
      <CircularProgress width={64} height={64} progress={percentage} />
      <div className="absolute left-0 top-0 flex h-full w-full items-center justify-center">
        <p className={cn("font-semibold", textSizeClass)}>{percentage}%</p>
      </div>
    </div>
  );
}

export function UserPage() {
  const { githubUsername } = useParams();

  const [metadata, setMetadata] = useState(null);

  /**
   * @param {string} event
   * @param {any} data
   */
  function handleEvent(event, data) {
    switch (event) {
      case "metadata":
        setMetadata(data);
        console.log("received metadata", data);
        break;
      default:
        break;
    }
  }

  useEffect(() => {
    const unsubscribe = initiateEventSource(githubUsername, handleEvent);

    return unsubscribe;
  }, [githubUsername]);

  return (
    <PageContainer>
      <Navbar />
      <div className="mx-auto flex w-full max-w-[800px] flex-1 flex-col gap-8 p-10 sm:flex-row">
        <div className="flex gap-4 sm:w-56 sm:flex-col">
          <Avatar className="h-24 w-24 sm:h-56 sm:w-56">
            {metadata && <AvatarImage src={metadata["avatar_url"]} />}
            <AvatarFallback />
          </Avatar>

          <div className="flex flex-col">
            <h1 className="text-2xl font-semibold">{metadata?.name}</h1>
            <h2 className="text-xl font-light text-muted-foreground">
              {metadata?.login}
            </h2>
          </div>
        </div>
        <div className="flex flex-1 flex-col gap-4">
          <Card>
            <CardHeader>
              <div className="flex flex-row justify-between">
                <div className="flex flex-col space-y-1.5">
                  <CardTitle>Impact</CardTitle>
                  <CardDescription>Card Description</CardDescription>
                </div>
                <ScoreIndicator percentage={12} />
              </div>
            </CardHeader>

            <CardContent>
              <p>Card Content</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <div className="flex flex-row justify-between">
                <div className="flex flex-col space-y-1.5">
                  <CardTitle>Experience</CardTitle>
                  <CardDescription>Card Description</CardDescription>
                </div>
                <ScoreIndicator percentage={40} />
              </div>
            </CardHeader>
            <CardContent>
              <p>Card Content</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <div className="flex flex-row justify-between">
                <div className="flex flex-col space-y-1.5">
                  <CardTitle>Quality</CardTitle>
                  <CardDescription>Card Description</CardDescription>
                </div>
                <ScoreIndicator percentage={60} />
              </div>
            </CardHeader>
            <CardContent>
              <p>Card Content</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <div className="flex flex-row justify-between">
                <div className="flex flex-col space-y-1.5">
                  <CardTitle>Quality</CardTitle>
                  <CardDescription>Card Description</CardDescription>
                </div>
                <ScoreIndicator percentage={100} />
              </div>
            </CardHeader>
            <CardContent>
              <p>Card Content</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </PageContainer>
  );
}
