import { Navbar } from "@/components/navbar";
import { PageContainer } from "@/components/page-container";
import { useState } from "react";
import mockData from "./sampleCompare";
import { useEffect } from "react";
import { compareProfiles } from "@/lib/api";
import { useParams } from "react-router-dom";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

function UserRow({ profile }) {
  return (
    <tr className="rounded-lg border bg-card text-card-foreground shadow-sm">
      <td>
        <Avatar>
          <AvatarImage />
          <AvatarFallback />
        </Avatar>
      </td>
      <td className="flex flex-col gap-1">
        <div>{profile.name}</div>
        <div>{profile.username}</div>
      </td>
      <td>{profile.readability}</td>
      <td>{profile.bestCodingPractices}</td>
      <td>{profile.maintainability}</td>
      <td>{profile.impact}</td>
      <td>{profile.experience}</td>
      <td>{profile.generalScore}</td>
    </tr>
  );
}

export function CompareResultsPage() {
  const { githubUsernames } = useParams();

  const [comparison, setComparison] = useState("");

  useEffect(() => {
    const usernames = githubUsernames.split(",");
    const abortController = new AbortController();

    compareProfiles(usernames, abortController.signal)
      .then((resp) => {
        setComparison(resp);
      })
      .catch((err) => {
        if (err.name === "AbortError") return;
        console.error(err);
      });

    return () => abortController.abort();
  }, [githubUsernames]);

  return (
    <PageContainer>
      <Navbar />
      <h1>Compare GitHub User Profiles</h1>
      <h1>Results</h1>
      {/* Container that wraps all the different inputs. */}
      <table>
        <thead>
          <tr>
            <th />
            <th />
            <th>Readability</th>
            <th>Best Practices</th>
            <th>Maintainability</th>
            <th>Impact</th>
            <th>Experience</th>
            <th>General</th>
          </tr>
        </thead>
        <tbody>
          {mockData.profileScores?.map((profile, key) => {
            return <UserRow key={profile.username} profile={profile} />;
          })}
        </tbody>
      </table>
    </PageContainer>
  );
}
