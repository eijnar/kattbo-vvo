// src/main.tsx (or src/index.tsx depending on your setup)

import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import { Auth0Provider } from "@auth0/auth0-react";
import { AuthProvider } from "./contexts/AuthContext";
import { LoadingProvider } from "./contexts/LoadingContext";
import config from "./config"
import "./index.css";
import 'leaflet/dist/leaflet.css';

const onRedirectCallback = (appState: any) => {
  window.history.replaceState(
    {},
    document.title,
    appState && appState.returnTo ? appState.returnTo : window.location.pathname
  );
};

const container = document.getElementById("root");
const root = createRoot(container!);

root.render(
  <React.StrictMode>
      <Auth0Provider
        domain={config.auth.domain}
        clientId={config.auth.clientId}
        authorizationParams={{
          redirect_uri: window.location.origin,
          audience: config.auth.audience,
          scope: config.auth.scope,
        }}
        onRedirectCallback={onRedirectCallback}
        useRefreshTokens={config.auth.useRefreshTokens}
      >
        <AuthProvider>
          <LoadingProvider>
            <App />
          </LoadingProvider>
        </AuthProvider>
      </Auth0Provider>
  </React.StrictMode>
);
