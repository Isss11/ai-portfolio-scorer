import { Navbar } from "@/components/navbar";
import { PageContainer } from "@/components/page-container";
import { Input } from "@/components/ui/input";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";

const formSchema = z.object({
  input: z.string(),
});

export function AnalyzePage() {
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

    let username;
    if (
      input.startsWith("github.com/") ||
      input.startsWith("https://github.com/")
    ) {
      username = input.split("/").at(-1);
    } else if (!input.includes("/")) {
      username = input;
    } else {
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
        <main className="mx-auto flex w-full max-w-[700px] flex-1 flex-col items-center justify-center gap-10 p-5">
          <h1 className="text-3xl font-bold">Analyze a GitHub user</h1>
          <div className="flex w-full flex-col gap-2">
            <Input
              placeholder="GitHub URL or username"
              {...form.register("input")}
            />
            {errors.input && (
              <span className="text-destructive">{errors.input.message}</span>
            )}
          </div>
        </main>
      </form>
    </PageContainer>
  );
}
