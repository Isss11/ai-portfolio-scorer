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
import { Skeleton } from "@/components/ui/skeleton";
import { ScoreIndicator } from "@/components/score-indicator";

function CardSkeleton() {
  return <Skeleton className="h-36" />;
}

export function UserPage() {
  const { githubUsername } = useParams();

  const [metadata, setMetadata] = useState(null);
  const [impact, setImpact] = useState(null);
  const [experience, setExperience] = useState(null);
  const [quality, setQuality] = useState(null);
  const [ability, setAbility] = useState(null);

  /**
   * @param {string} event
   * @param {any} data
   */
  function handleEvent(event, data) {
    console.log("received", event, data);
    switch (event) {
      case "metadata":
        setMetadata(data);
        break;
      case "impact":
        setImpact(data);
        break;
      case "experience":
        setExperience(data);
        break;
      case "quality":
        setQuality(data);
        break;
      case "ability":
        setAbility(data);
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
          {impact ? (
            <Card>
              <CardHeader>
                <div className="flex flex-row justify-between">
                  <div className="flex flex-col space-y-1.5">
                    <CardTitle>Impact</CardTitle>
                    <CardDescription>
                      Popularity, open-source contributions
                    </CardDescription>
                  </div>
                  <ScoreIndicator percentage={impact.score} />
                </div>
              </CardHeader>

              {impact.feedback.length > 0 && (
                <CardContent>
                  <ul className="flex list-disc flex-col gap-1 pl-4">
                    {impact.feedback.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </CardContent>
              )}
            </Card>
          ) : (
            <CardSkeleton />
          )}
          {experience ? (
            <Card>
              <CardHeader>
                <div className="flex flex-row justify-between">
                  <div className="flex flex-col space-y-1.5">
                    <CardTitle>Experience</CardTitle>
                    <CardDescription>
                      Expertise & familiarity with languages and tools
                    </CardDescription>
                  </div>
                  <ScoreIndicator percentage={experience.score} />
                </div>
              </CardHeader>

              {experience.feedback.length > 0 && (
                <CardContent>
                  <ul className="flex list-disc flex-col gap-1 pl-4">
                    {experience.feedback.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </CardContent>
              )}
            </Card>
          ) : (
            <CardSkeleton />
          )}
          {quality ? (
            <Card>
              <CardHeader>
                <div className="flex flex-row justify-between">
                  <div className="flex flex-col space-y-1.5">
                    <CardTitle>Quality</CardTitle>
                    <CardDescription>
                      Readability, maintainability, best practices
                    </CardDescription>
                  </div>
                  <ScoreIndicator percentage={quality.score} />
                </div>
              </CardHeader>

              {quality.feedback.length > 0 && (
                <CardContent>
                  <ul className="flex list-disc flex-col gap-1 pl-4">
                    {quality.feedback.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </CardContent>
              )}
            </Card>
          ) : (
            <CardSkeleton />
          )}
          {ability ? (
            <Card>
              <CardHeader>
                <div className="flex flex-row justify-between">
                  <div className="flex flex-col space-y-1.5">
                    <CardTitle>Technical ability</CardTitle>
                    <CardDescription>
                      Adaptability, problem-solving, proficiency
                    </CardDescription>
                  </div>
                  <ScoreIndicator percentage={ability.score} />
                </div>
              </CardHeader>

              {ability.feedback.length > 0 && (
                <CardContent>
                  <ul className="flex list-disc flex-col gap-1 pl-4">
                    {ability.feedback.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </CardContent>
              )}
            </Card>
          ) : (
            <CardSkeleton />
          )}
        </div>
      </div>
    </PageContainer>
  );
}
