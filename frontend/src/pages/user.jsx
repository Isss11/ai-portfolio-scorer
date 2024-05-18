import { Navbar } from "@/components/navbar";
import { PageContainer } from "@/components/page-container";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { initiateEventSource } from "@/lib/api";
import { useState } from "react";
import { useEffect } from "react";
import { useParams } from "react-router-dom";

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
      <div className="mx-auto flex w-full max-w-[700px] flex-1 p-5">
        <div className="flex w-56 flex-col gap-4">
          <Avatar className="h-56 w-56">
            {metadata && <AvatarImage src={metadata["avatar_url"]} />}
            <AvatarFallback />
          </Avatar>

          <h1 className="text-2xl font-semibold">{metadata?.name}</h1>
        </div>
        <div className="flex flex-1 flex-col"></div>
      </div>
    </PageContainer>
  );
}
