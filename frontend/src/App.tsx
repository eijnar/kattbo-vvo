import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ApmRoutes } from "./apm";
import Navbar from "./components/common/Navbar";
import LandingPage from "./pages/LandingPage";
import ProfilePage from "./pages/ProfilePage";
import ListUsers from "./pages/ListUsersPage";
import CreateApiKey from "./components/apiKeys/CreateApiKey";
import LoginPage from "./pages/LoginPage";
import ProtectedRoute from "./components/common/ProtectedRoute";

const App: React.FC = () => {
  return (
    <Router>
      <Navbar />
      <ApmRoutes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/users" element={<ListUsers />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/create-api-key" element={<CreateApiKey />} />
          <Route
            path="/profile"
            element={<ProtectedRoute component={ProfilePage} />}
          />
        </ApmRoutes>
    </Router>
  );
};

export default App;
