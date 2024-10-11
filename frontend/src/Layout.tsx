import { Outlet } from "react-router-dom";
import Navbar from "./components/core/Navbar/Navbar";
import { useTitle } from "./contexts/TitleContext";

const Layout = () => {
  const { title } = useTitle();

  return (
    <div className="min-h-screen w-full bg-gray-200">
      <Navbar />
      <div className="pt-16">
        <header className="bg-white shadow">
          <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900">
              {title}
            </h1>
          </div>
        </header>
        <main>
          <div className="mx-auto max-w-7xl sm:px-0 lg:px-1">
          <div className="max-w-5xl mx-auto p-6 space-y-8">
            <Outlet />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
