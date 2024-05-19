import { Navbar } from "@/components/navbar";
import { PageContainer } from "@/components/page-container";
import { Input } from "@/components/ui/input";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import { parseGithubUsername } from "@/lib/utils";
import { Button } from "@/components/ui/button";

const formSchema = z.object({
  input: z.string(),
});

export function HomePage() {
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      input: "",
    },
  });

  const navigate = useNavigate();

  function onSubmit(data) {
    const { input } = data;

    if (!input) {
      return;
    }

    const username = parseGithubUsername(input);
    if (!username) {
      form.setError("input", { message: "Invalid GitHub URL or username" });
      return;
    }

    navigate(`/user/${username}`);
  }

  const { errors } = form.formState;

  return (
    <PageContainer>
      <Navbar />

      <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-1">
        <main className="mx-auto flex w-full max-w-[500px] flex-1 flex-col items-stretch justify-center gap-10 p-5 text-center">
          <h1 className="text-4xl font-bold">Evaluate GitHub Portfolios using AI.</h1>
          <h2 className="text-3xl font-bold">Analyze a GitHub User</h2>
          <div className="flex w-full flex-col gap-2">
            <Input
              placeholder="GitHub URL or username"
              {...form.register("input")}
            />
            {errors.input && (
              <span className="text-destructive">{errors.input.message}</span>
            )}
          </div>
          <Button type="submit">Analyze</Button>
        </main>
      </form>
    </PageContainer>
  );
}
