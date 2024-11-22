const requiredEnvVariables = [
    'VITE_ENVIRONMENT',
    'VITE_APM_SERVICE_NAME',
    'VITE_APM_SERVER_URL',
    'VITE_APM_DISTRIBUTED_TRACING_ORIGINS',
    'VITE_APM_LOG_LEVEL',
    'VITE_APM_TRANSACTION_SAMPLE_RATE',
    'VITE_AUTH_DOMAIN',
    'VITE_AUTH_CLIENT_ID',
    'VITE_AUTH_REDIRECT_URI',
    'VITE_AUTH_AUDIENCE',
    'VITE_AUTH_SCOPE',
    'VITE_AUTH_USE_REFRESH_TOKENS',
];

requiredEnvVariables.forEach((varName) => {
    if (!import.meta.env[varName]) {
        console.warn(`Warning: Missing environment variable ${varName}`);
        // Optionally, throw an error to prevent the app from running
        // throw new Error(`Missing required environment variable: ${varName}`);
    }
});

const config = {
    general: {
        environment: import.meta.env.ENVIRONMENT,
    },
    apm: {
        serviceName: import.meta.env.VITE_APM_SERVICE_NAME,
        serverUrl: import.meta.env.VITE_APM_SERVER_URL,
        distributedTracingOrigins: import.meta.env.VITE_APM_DISTRIBUTED_TRACING_ORIGINS            
            ? import.meta.env.VITE_APM_DISTRIBUTED_TRACING_ORIGINS.split(',')
            : [],
        logLevel: import.meta.env.VITE_APM_LOG_LEVEL,
        transactionSampleRate: import.meta.env.VITE_APM_TRANSACTION_SAMPLE_RATE
            ? parseFloat(import.meta.env.VITE_APM_TRANSACTION_SAMPLE_RATE)
            : 1.0,
    },
    auth: {
        domain: import.meta.env.VITE_AUTH_DOMAIN,
        clientId: import.meta.env.VITE_AUTH_CLIENT_ID,
        authorizationParams: {
            redirect_uri: import.meta.env.VITE_AUTH_REDIRECT_URI,
        },
        audience: import.meta.env.VITE_AUTH_AUDIENCE,
        useRefreshTokens: import.meta.env.VITE_AUTH_USE_REFRESH_TOKENS,
        scope: import.meta.env.VITE_AUTH_SCOPE
            ? import.meta.env.VITE_AUTH_SCOPE.split(',')
            : [],
    },
};

export default config;