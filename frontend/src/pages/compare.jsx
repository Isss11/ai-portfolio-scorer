import { Navbar } from "@/components/navbar";
import { PageContainer } from "@/components/page-container";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { useNavigate } from "react-router-dom";
import { isNotNullish, parseGithubUsername } from "@/lib/utils";

export function ComparePage() {
  const [textareaValue, setTextareaValue] = useState("");
  const navigate = useNavigate();

  /** @param {React.FormEvent} e */
  const handleSubmit = async (e) => {
    e.preventDefault();

    const usernames = textareaValue
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0)
      .map(parseGithubUsername)
      .filter(isNotNullish)
      .filter((username, idx, arr) => arr.indexOf(username) === idx);

    if (usernames.length < 2) {
      return;
    }

    const usernamesString = usernames.join(",");

    navigate(`/compare/${usernamesString}`);
  };

  return (
    <PageContainer>
      <Navbar />
      <h1>Compare GitHub User Profiles</h1>
      <form onSubmit={handleSubmit}>
        <Textarea
          rows="4"
          // cols="10"
          value={textareaValue}
          onChange={(e) => setTextareaValue(e.target.value)}
          placeholder="Enter a list of users' GitHub profile URLs, with each URL on a separate line."
        />
        <Button type="submit">Compare Profiles</Button>
      </form>
    </PageContainer>
  );
}
