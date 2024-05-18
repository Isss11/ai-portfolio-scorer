import { HomePage } from "./pages/home.jsx";
import { AnalyzePage } from "./pages/analyze.jsx";
import { RouterProvider, createBrowserRouter } from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/analyze",
    element: <AnalyzePage />,
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
