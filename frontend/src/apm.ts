import { init as initApm } from '@elastic/apm-rum';

const apm = initApm({
  serviceName: 'kattbo-vvo-api',
  serverUrl: 'http://riker.srv.kaffesump.se:8200', // APM Server URL
  environment: 'development', // or 'development'
  distributedTracingOrigins: ['http://127.0.0.1:8000'],
  logLevel: 'debug', // Set log level to debug
});

export default apm;