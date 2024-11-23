import type { LogLevel } from "./types/types";

interface Config {
  general: {
    environment: string;
  };
  apm: {
    serviceName: string;
    serverUrl: string;
    distributedTracingOrigins: string[];
    logLevel: LogLevel;
    transactionSampleRate: number;
  };
  auth: {
    domain: string;
    clientId: string;
    authorizationParams: {
      redirect_uri: string;
    };
    audience: string;
    scope: string;
    useRefreshTokens: boolean;
  };
}

const config: Config = {
  general: {
    environment: "development",
  },
  apm: {
    serviceName: "Kattbo_VVO-Frontend",
    serverUrl: "https://apm.elastic.morbit.se",
    distributedTracingOrigins: ["https://dev-api.kattbovvo.se"],
    logLevel: "debug",
    transactionSampleRate: 1.0,
  },
  auth: {
    domain: "auth.kattbovvo.se",
    clientId: "kL1RLUxgfsVZBa7vVKgry2Eyq8taK1pA",
    authorizationParams: {
      redirect_uri: "http://dev.kattbovvo.se/",
    },
    audience: "https://dev-api.kattbovvo.se",
    useRefreshTokens: true,
    scope: "user:read user:del",
  },
};

export default config;
