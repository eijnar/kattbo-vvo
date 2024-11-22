import { init as initApm } from '@elastic/apm-rum';
import { ApmRoutes } from '@elastic/apm-rum-react'

const apm = initApm({
  serviceName: 'Kattbo_VVO-Frontend',
  serverUrl: 'http://riker.srv.kaffesump.se:8200', // APM Server URL
  environment: 'development', // or 'development'
  distributedTracingOrigins: ['https://dev-api.kattbovvo.se'],
  logLevel: 'debug', // Set log level to debug
  transactionSampleRate: 1.0,
});

export { apm, ApmRoutes };