import { ModuleFederationConfig } from '@nx/module-federation';

const config: ModuleFederationConfig = {
  name: 'hr-shell',
  remotes: ['admin-portal', 'employee-self-service'],
};

export default config;
