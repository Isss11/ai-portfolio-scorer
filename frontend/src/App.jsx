import { ComparePage } from "./pages/compare.jsx";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import { AnalyzePage } from "./pages/analyze.jsx";
import { UserPage } from "./pages/user.jsx";
import { CompareResultsPage } from "./pages/compare-results.jsx";

const router = createBrowserRouter([
  {
    path: "/analyze",
    element: <AnalyzePage />,
  },
  {
    path: "/compare",
    element: <ComparePage />,
  },
  {
    path: "/user/:githubUsername",
    element: <UserPage />,
  },
  {
    path: "/compare/:githubUsernames",
    element: <CompareResultsPage />,
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
