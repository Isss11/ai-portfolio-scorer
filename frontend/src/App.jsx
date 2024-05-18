import { ComparePage } from "./pages/compare.jsx"
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import { HomePage } from "./pages/home.jsx";
import { AnalyzePage } from "./pages/analyze.jsx";
import { UserPage } from "./pages/user.jsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/analyze",
    element: <AnalyzePage />,
  },
  {
    path: "/compare",
    element: <ComparePage />
  },
  {
    path: "/user/:githubUsername",
    element: <UserPage />,
  },
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
      <Toaster />
    </>
  );
}

export default App;
