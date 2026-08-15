import { ModuleFederationConfig } from '@nx/module-federation';

const config: ModuleFederationConfig = {
  name: 'employee-self-service',
  exposes: {
    './Routes': 'apps/employee-self-service/src/app/remote-entry/entry.routes.ts',
  },
};

export default config;
