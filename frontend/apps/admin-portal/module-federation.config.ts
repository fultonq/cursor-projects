import { ModuleFederationConfig } from '@nx/module-federation';

const config: ModuleFederationConfig = {
  name: 'admin-portal',
  exposes: {
    './Routes': 'apps/admin-portal/src/app/remote-entry/entry.routes.ts',
  },
};

export default config;
