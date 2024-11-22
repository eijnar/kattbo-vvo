import { init as initApm } from '@elastic/apm-rum';
import { ApmRoutes } from '@elastic/apm-rum-react'
import config from './config'


const apm = initApm({
  serviceName: config.apm.serviceName,
  serverUrl: config.apm.serverUrl,
  environment: config.general.environment,
  distributedTracingOrigins: config.apm.distributedTracingOrigins,
  logLevel: config.apm.logLevel,
  transactionSampleRate: config.apm.transactionSampleRate,
});

export { apm, ApmRoutes };