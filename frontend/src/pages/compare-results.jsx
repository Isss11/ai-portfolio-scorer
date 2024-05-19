import { Navbar } from "@/components/navbar";
import { PageContainer } from "@/components/page-container";
import { useState } from "react";
import { useEffect } from "react";
import { compareProfiles } from "@/lib/api";
import { useParams } from "react-router-dom";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { Skeleton } from "@/components/ui/skeleton";
import { ScoreIndicator } from "@/components/score-indicator";
import { formatRanking } from "@/lib/format";
import { useNavigate } from "react-router-dom";

function UserRow({ userData, score, rank }) {
  const navigate = useNavigate();

  return (
    <tr
      className={cn(
        "rounded-lg bg-card p-4 text-card-foreground shadow-sm outline outline-1 outline-border",
        userData && "cursor-pointer",
      )}
      onClick={userData ? () => navigate(`/user/${userData.login}`) : undefined}
    >
      <Cell className="w-14 text-end text-sm text-muted-foreground">
        {userData ? (
          formatRanking(rank)
        ) : (
          <Skeleton className="ml-auto h-5 w-6" />
        )}
      </Cell>
      <Cell className="w-16">
        <Avatar className="h-16 w-16">
          <AvatarImage src={userData?.["avatar_url"]} />
          <AvatarFallback />
        </Avatar>
      </Cell>
      <Cell>
        {userData ? (
          <h1>{userData.name}</h1>
        ) : (
          <Skeleton className="mb-1 h-5 w-40" />
        )}
        {userData ? (
          <h2 className="text-sm font-light text-muted-foreground">
            {userData.login}
          </h2>
        ) : (
          <Skeleton className="h-4 w-20" />
        )}
      </Cell>
      <Cell className="w-24">
        {userData ? (
          <ScoreIndicator percentage={score} />
        ) : (
          <Skeleton className="h-[50px] w-[50px] rounded-full" />
        )}
      </Cell>
    </tr>
  );
}

function HeaderCell({ className, ...props }) {
  return <th className={cn("p-2 text-start sm:p-3", className)} {...props} />;
}

function Cell({ className, ...props }) {
  return <td className={cn("h-20 p-2 sm:p-3", className)} {...props} />;
}

export function CompareResultsPage() {
  const { githubUsernames } = useParams();
  const usernames = githubUsernames.split(",");

  const [comparison, setComparison] = useState("");

  useEffect(() => {
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
      <div className="mx-auto flex w-full max-w-[800px] flex-col gap-8 p-10">
        <h1 className="text-4xl font-bold">GitHub Profile Comparison</h1>

        {/* <div className="flex h-40 items-end justify-center">
          <div className="relative flex h-2/3 w-24 items-center justify-center bg-muted text-xl font-semibold">
            <div className="absolute -top-6 mx-auto">
              <Avatar className="h-12 w-12">
                <AvatarImage src={comparison?.[1]?.["user_data"]?.avatar_url} />
                <AvatarFallback />
              </Avatar>
            </div>
            2
          </div>
          <div className="relative flex h-full w-24 items-center justify-center bg-muted text-xl font-semibold">
            <div className="absolute -top-6 mx-auto">
              <Avatar className="h-12 w-12">
                <AvatarImage src={comparison?.[0]?.["user_data"]?.avatar_url} />
                <AvatarFallback />
              </Avatar>
            </div>
            1
          </div>
          <div className="relative flex h-1/3 w-24 items-center justify-center bg-muted text-xl font-semibold">
            <div className="absolute -top-6 mx-auto">
              <Avatar className="h-12 w-12">
                <AvatarImage src={comparison?.[2]?.["user_data"]?.avatar_url} />
                <AvatarFallback />
              </Avatar>
            </div>
            3
          </div>
        </div> */}

        <table className="table-fixed border-separate border-spacing-y-2">
          <thead>
            <tr>
              <HeaderCell className="w-14" />
              <HeaderCell className="w-16">User</HeaderCell>
              <HeaderCell />
              <HeaderCell className="w-24">Score</HeaderCell>
            </tr>
          </thead>
          <tbody>
            {comparison
              ? comparison.map((user, idx) => (
                  <UserRow
                    key={user["user_data"].login}
                    userData={user["user_data"]}
                    score={user["score"]}
                    rank={idx + 1}
                  />
                ))
              : usernames.map((username) => (
                  <UserRow key={username} userData={undefined} />
                ))}
          </tbody>
        </table>
      </div>
    </PageContainer>
  );
}
