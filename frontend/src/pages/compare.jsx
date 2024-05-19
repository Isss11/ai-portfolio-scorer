import { Navbar } from "@/components/navbar";
import { PageContainer } from "@/components/page-container";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import { isNotNullish, parseGithubUsername } from "@/lib/utils";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

const formSchema = z.object({
  input: z.string(),
});

export function ComparePage() {
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      input: "",
    },
  });

  const navigate = useNavigate();

  function onSubmit(data) {
    const { input } = data;

    const usernames = input
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0)
      .map(parseGithubUsername)
      .filter(isNotNullish)
      .filter((username, idx, arr) => arr.indexOf(username) === idx);

    if (usernames.length < 2) {
      form.setError("input", {
        message: "Please enter at least two valid GitHub URLs or usernames",
      });
      return;
    }

    const usernamesString = usernames.join(",");

    navigate(`/compare/${usernamesString}`);
  }

  const { errors } = form.formState;

  return (
    <PageContainer>
      <Navbar />
      <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-1">
        <main className="mx-auto flex w-full max-w-[700px] flex-1 flex-col items-stretch justify-center gap-10 p-5 text-center">
          <h1 className="text-3xl font-bold">Compare GitHub user profiles</h1>
          <div className="flex w-full flex-col gap-2">
            <Textarea
              rows="4"
              placeholder="Enter a list of users' GitHub profile URLs, with each URL on a separate line."
              {...form.register("input")}
            />
            {errors.input && (
              <span className="text-destructive">{errors.input.message}</span>
            )}
          </div>
          <Button type="submit">Compare Profiles</Button>
        </main>
      </form>
    </PageContainer>
  );
}
