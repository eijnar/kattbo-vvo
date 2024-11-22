export interface APMConfig {
    serviceName: string;
    serverUrl: string;
    environment: string;
    distributedTracingOrigins: string[];
    logLevel: 'debug' | 'info' | 'warn' | 'error';
    transactionSampleRate: number;
  }
  
  export interface AuthConfig {
    domain: string;
    clientId: string;
    authorizationParams: {
      redirect_uri: string;
    };
    audience: string;
    scope: string;
    useRefreshTokens: boolean;
  }
  
  export interface Config {
    apm: APMConfig;
    auth: AuthConfig;
  }