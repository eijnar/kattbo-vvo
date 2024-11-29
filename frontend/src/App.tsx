import React from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import { ApmRoutes } from "./apm";
import LandingPage from "./pages/LandingPage";
import ProfilePage from "./pages/ProfilePage";
import CreateApiKey from "./components/apiKeys/CreateApiKey";
import LoginPage from "./pages/LoginPage";
import ProtectedRoute from "./components/common/ProtectedRoute";
import Layout from "./components/Layout";
import Map from "./components/map/Map";
import TeamPage from "./pages/TeamPage";
import EventListPage from "./pages/EventList";

const App: React.FC = () => {
  return (
    <Router>
      <ApmRoutes>
        <Route element={<Layout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/hunting_team" element={<TeamPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/event" element={<EventListPage />} />
          <Route path="/map" element={<Map />} />
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
