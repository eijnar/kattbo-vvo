import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import { ApmRoutes } from "./apm";
import LandingPage from "./pages/LandingPage";
import ProfilePage from "./pages/ProfilePage";
import ListUsers from "./pages/ListUsersPage";
import CreateApiKey from "./components/apiKeys/CreateApiKey";
import LoginPage from "./pages/LoginPage";
import ProtectedRoute from "./components/common/ProtectedRoute";
import Layout from "./components/Layout";

const App: React.FC = () => {
  return (
    <Router>
      <ApmRoutes>
        <Route element={<Layout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/users" element={<ListUsers />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/api-keys" element={<CreateApiKey />} />
          <Route
            path="/profile"
            element={<ProtectedRoute component={ProfilePage} />}
          />
        </Route>
      </ApmRoutes>
    </Router>
  );
};

export default App;
