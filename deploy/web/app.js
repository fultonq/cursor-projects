const app = document.getElementById("app");

const shell = (main) => `
  <p class="hr-banner">Render demo · mock data · tenant Aether Dynamics · region EMEA</p>
  <header class="hr-top">
    <a class="hr-brand" href="/">Aether HR</a>
    <input class="hr-search" placeholder="Search people, jobs, tickets…" readonly />
    <span class="hr-chip">Aether Dynamics</span>
    <span class="hr-chip">EMEA</span>
    <nav class="hr-row">
      <a href="/">Home</a>
      <a href="/admin">Admin</a>
      <a href="/ess">Self-service</a>
    </nav>
    <span class="hr-avatar">PN</span>
  </header>
  ${main}
`;

const admin = (active, inner) =>
  shell(`
  <div class="hr-app">
    <aside class="hr-side">
      <p class="hr-brand" style="padding: 0 0.75rem 0.75rem">Admin Portal</p>
      <a href="/admin" class="${active === "overview" ? "on" : ""}">Overview</a>
      <a href="/admin/directory" class="${active === "directory" ? "on" : ""}">Directory</a>
      <a href="/admin/org" class="${active === "org" ? "on" : ""}">Org chart</a>
      <a href="/admin/recruitment" class="${active === "recruitment" ? "on" : ""}">Recruitment</a>
      <a href="/admin/payroll" class="${active === "payroll" ? "on" : ""}">Payroll</a>
      <a href="/admin/access" class="${active === "access" ? "on" : ""}">Access</a>
    </aside>
    <section class="hr-main">${inner}</section>
  </div>
`);

const ess = (active, inner) =>
  shell(`
  <div class="hr-app">
    <aside class="hr-side">
      <p class="hr-brand" style="padding: 0 0.75rem 0.75rem">Self-service</p>
      <a href="/ess" class="${active === "work" ? "on" : ""}">Workspace</a>
      <a href="/ess/profile" class="${active === "profile" ? "on" : ""}">Profile</a>
      <a href="/ess/time-off" class="${active === "time" ? "on" : ""}">Time off</a>
      <a href="/ess/payslips" class="${active === "pay" ? "on" : ""}">Payslips</a>
    </aside>
    <section class="hr-main">${inner}</section>
  </div>
`);

const pages = {
  "/login": () => `
    <section class="hr-login">
      <aside class="hr-login-hero">
        <p class="hr-brand">Aether HR</p>
        <h1>Global workforce, region-isolated.</h1>
        <p>25,412 principals · OIDC + SAML · AMER · EMEA · APAC</p>
        <div class="hr-row" style="margin-top: 1.5rem">
          <span class="hr-chip">AMER</span><span class="hr-chip">EMEA</span><span class="hr-chip">APAC</span>
        </div>
      </aside>
      <div class="hr-login-form">
        <div class="hr-card hr-login-card">
          <h2 class="hr-h1">Sign in to your workspace</h2>
          <p class="hr-sub">Continue with your company identity provider.</p>
          <label>Work email</label>
          <input class="hr-field" value="priya.nair@aetherdynamics.com" readonly />
          <label>Tenant ID</label>
          <input class="hr-field" value="AETHER-GLOBAL" readonly />
          <a class="hr-btn" href="/">Continue with company SSO</a>
          <p class="hr-sub" style="margin-top: 1rem">Use SAML IdP · Use recovery code</p>
        </div>
      </div>
    </section>
  `,
  "/": () =>
    shell(`
    <section class="hr-main">
      <h1 class="hr-h1">Good morning, Priya</h1>
      <p class="hr-sub">People Partner · London · EMEA shard · hosted on Render</p>
      <div class="hr-kpis">
        <article class="hr-card hr-kpi"><span>Headcount</span><strong>25,412</strong></article>
        <article class="hr-card hr-kpi"><span>Open requisitions</span><strong>186</strong></article>
        <article class="hr-card hr-kpi"><span>Payroll runs in progress</span><strong>3</strong></article>
        <article class="hr-card hr-kpi"><span>Compliance alerts</span><strong>7</strong></article>
      </div>
      <div class="hr-grid-2">
        <div class="hr-tiles">
          <a class="hr-card hr-tile" href="/admin">
            <span class="hr-chip">Admin Portal</span>
            <h2>Workforce operations</h2>
            <p class="hr-sub">Directory, org chart, payroll, recruitment, IAM.</p>
          </a>
          <a class="hr-card hr-tile" href="/ess">
            <span class="hr-chip">Self-service</span>
            <h2>Employee workspace</h2>
            <p class="hr-sub">Profile, time off, payslips, benefits.</p>
          </a>
        </div>
        <article class="hr-card">
          <h3>Regional pulse</h3>
          <table class="hr-table">
            <thead><tr><th>Region</th><th>Headcount</th><th>Shard</th></tr></thead>
            <tbody>
              <tr><td>AMER</td><td>9,840</td><td>pg-amer</td></tr>
              <tr><td>EMEA</td><td>10,205</td><td>pg-emea</td></tr>
              <tr><td>APAC</td><td>5,367</td><td>pg-apac</td></tr>
            </tbody>
          </table>
        </article>
      </div>
    </section>
  `),
  "/admin": () =>
    admin(
      "overview",
      `
      <h1 class="hr-h1">Workforce operations</h1>
      <p class="hr-sub">Tenant AETHER-GLOBAL · mock data</p>
      <div class="hr-kpis">
        <article class="hr-card hr-kpi"><span>Active employees</span><strong>25,412</strong></article>
        <article class="hr-card hr-kpi"><span>New hires (30d)</span><strong>214</strong></article>
        <article class="hr-card hr-kpi"><span>Attrition</span><strong>0.8%</strong></article>
        <article class="hr-card hr-kpi"><span>Time-to-fill</span><strong>31d</strong></article>
      </div>
      <div class="hr-grid-2">
        <article class="hr-card">
          <h3>Region shards</h3>
          <table class="hr-table">
            <thead><tr><th>Region</th><th>Headcount</th><th>Database</th></tr></thead>
            <tbody>
              <tr><td>AMER</td><td>9,840</td><td>hr_amer</td></tr>
              <tr><td>EMEA</td><td>10,205</td><td>hr_emea</td></tr>
              <tr><td>APAC</td><td>5,367</td><td>hr_apac</td></tr>
            </tbody>
          </table>
        </article>
        <article class="hr-card">
          <h3>Attention required</h3>
          <table class="hr-table">
            <tbody>
              <tr><td>EMEA payroll calendar locked</td><td><span class="hr-pill warn">Cutoff</span></td></tr>
              <tr><td>APAC tax table stale (SG)</td><td><span class="hr-pill bad">Tax</span></td></tr>
              <tr><td>SAML cert expires in 18 days</td><td><span class="hr-pill warn">IAM</span></td></tr>
              <tr><td>GDPR DSAR queue · 4 open</td><td><span class="hr-pill">Audit</span></td></tr>
            </tbody>
          </table>
        </article>
      </div>
    `
    ),
  "/admin/directory": () =>
    admin(
      "directory",
      `
      <h1 class="hr-h1">Employee directory</h1>
      <p class="hr-sub">25,412 records · virtualized · region EMEA</p>
      <article class="hr-card">
        <table class="hr-table">
          <thead><tr><th>Employee</th><th>ID</th><th>Title</th><th>Location</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td>Priya Nair</td><td>EMP-104829</td><td>People Partner</td><td>London</td><td><span class="hr-pill ok">Active</span></td></tr>
            <tr><td>Jonas Weber</td><td>EMP-100214</td><td>VP Engineering</td><td>Berlin</td><td><span class="hr-pill ok">Active</span></td></tr>
            <tr><td>Marcus Holm</td><td>EMP-188204</td><td>Staff Engineer</td><td>Stockholm</td><td><span class="hr-pill ok">Active</span></td></tr>
            <tr><td>Amelia Chen</td><td>EMP-100001</td><td>Chief Executive Officer</td><td>London</td><td><span class="hr-pill ok">Active</span></td></tr>
            <tr><td>Leila Haddad</td><td>EMP-176330</td><td>Staff Engineer</td><td>Paris</td><td><span class="hr-pill ok">Active</span></td></tr>
            <tr><td>Sofia Alvarez</td><td>EMP-155902</td><td>Payroll Analyst</td><td>Madrid</td><td><span class="hr-pill ok">Active</span></td></tr>
          </tbody>
        </table>
      </article>
    `
    ),
  "/admin/org": () =>
    admin(
      "org",
      `
      <h1 class="hr-h1">Organization · Product Engineering</h1>
      <p class="hr-sub">EMEA forest · cross-region managers are correlation IDs</p>
      <div class="hr-org">
        <article class="hr-card hr-person"><div class="hr-avatar" style="margin: 0 auto 0.4rem">AC</div><strong>Amelia Chen</strong><p class="hr-sub">Chief Executive Officer</p></article>
        <div class="hr-org-row">
          <article class="hr-card hr-person"><div class="hr-avatar" style="margin: 0 auto 0.4rem">JW</div><strong>Jonas Weber</strong><p class="hr-sub">VP Engineering · 186</p></article>
          <article class="hr-card hr-person"><div class="hr-avatar" style="margin: 0 auto 0.4rem">PN</div><strong>Priya Nair</strong><p class="hr-sub">People Partner · 24</p></article>
          <article class="hr-card hr-person"><div class="hr-avatar" style="margin: 0 auto 0.4rem">SA</div><strong>Sofia Alvarez</strong><p class="hr-sub">Payroll Ops · 12</p></article>
        </div>
      </div>
    `
    ),
  "/admin/recruitment": () =>
    admin(
      "recruitment",
      `
      <h1 class="hr-h1">Recruitment pipeline</h1>
      <p class="hr-sub">186 open requisitions · offer accept 71%</p>
      <div class="hr-kanban">
        ${[
          ["Sourcing", "Owen Blake", "HRBP"],
          ["Screen", "Mia Rossi", "Payroll Analyst"],
          ["Interview", "Leila Haddad", "Staff Engineer"],
          ["Offer", "Hannah Cole", "Recruiter"],
          ["Hired", "Kenji Sato", "Eng Manager"],
        ]
          .map(
            ([name, person, role]) => `
          <div class="hr-col"><strong>${name}</strong>
            <article class="hr-card" style="margin-top: 0.5rem"><div>${person}</div><p class="hr-sub">${role}</p></article>
          </div>`
          )
          .join("")}
      </div>
    `
    ),
  "/admin/payroll": () =>
    admin(
      "payroll",
      `
      <h1 class="hr-h1">Payroll runs · August 2026</h1>
      <p class="hr-sub">No cross-region posting — each run stays on its shard.</p>
      <div class="hr-kpis">
        <article class="hr-card hr-kpi"><span>AMER · USD</span><strong>62%</strong></article>
        <article class="hr-card hr-kpi"><span>EMEA · EUR</span><strong>Queued</strong></article>
        <article class="hr-card hr-kpi"><span>APAC · SGD</span><strong>Validate</strong></article>
        <article class="hr-card hr-kpi"><span>Pay groups</span><strong>18</strong></article>
      </div>
    `
    ),
  "/admin/access": () =>
    admin(
      "access",
      `
      <h1 class="hr-h1">Identity & access</h1>
      <p class="hr-sub">Region claim is not a tenant. Residency is enforced by X-Region.</p>
      <article class="hr-card">
        <table class="hr-table">
          <thead><tr><th>Role</th><th>Principals</th><th>Permissions</th></tr></thead>
          <tbody>
            <tr><td>People Partner</td><td>86</td><td>directory:read</td></tr>
            <tr><td>Payroll Ops Lead</td><td>14</td><td>payroll:run</td></tr>
            <tr><td>Recruiter</td><td>41</td><td>offer:draft</td></tr>
            <tr><td>Engineering Manager</td><td>312</td><td>offer:approve</td></tr>
            <tr><td>Compliance Officer</td><td>9</td><td>audit:read</td></tr>
          </tbody>
        </table>
      </article>
    `
    ),
  "/ess": () =>
    ess(
      "work",
      `
      <h1 class="hr-h1">Your Friday snapshot</h1>
      <p class="hr-sub">Marcus Holm · Staff Engineer · Stockholm · EMEA</p>
      <div class="hr-kpis">
        <article class="hr-card hr-kpi"><span>Time off balance</span><strong>18.5d</strong></article>
        <article class="hr-card hr-kpi"><span>Next payday</span><strong>31 Aug</strong></article>
        <article class="hr-card hr-kpi"><span>Goals</span><strong>3 / 5</strong></article>
        <article class="hr-card hr-kpi"><span>Last net pay</span><strong>€4,820</strong></article>
      </div>
      <div class="hr-row">
        <a class="hr-btn" href="/ess/time-off">Request time off</a>
        <a class="hr-btn ghost" href="/ess/payslips">View payslip</a>
        <a class="hr-btn ghost" href="/ess/profile">Update address</a>
      </div>
    `
    ),
  "/ess/profile": () =>
    ess(
      "profile",
      `
      <h1 class="hr-h1">Profile</h1>
      <p class="hr-sub">Workforce master data is read-only here.</p>
      <article class="hr-card">
        <table class="hr-table">
          <tbody>
            <tr><td>Employee ID</td><td>EMP-188204</td></tr>
            <tr><td>Title</td><td>Staff Engineer</td></tr>
            <tr><td>Manager</td><td>Jonas Weber</td></tr>
            <tr><td>Location</td><td>Stockholm</td></tr>
            <tr><td>Region</td><td>EMEA</td></tr>
          </tbody>
        </table>
      </article>
    `
    ),
  "/ess/time-off": () =>
    ess(
      "time",
      `
      <h1 class="hr-h1">Time off</h1>
      <p class="hr-sub">Approver: Jonas Weber · balance 18.5 days</p>
      <article class="hr-card">
        <label>Type</label>
        <input class="hr-field" value="Vacation" readonly />
        <label>Dates</label>
        <input class="hr-field" value="8 Sep 2026 – 12 Sep 2026" readonly />
        <button class="hr-btn" type="button">Submit request</button>
      </article>
    `
    ),
  "/ess/payslips": () =>
    ess(
      "pay",
      `
      <h1 class="hr-h1">Payslip · July 2026</h1>
      <p class="hr-sub">Stored in the EMEA region shard (GDPR).</p>
      <article class="hr-card">
        <table class="hr-table">
          <tbody>
            <tr><td>Employee</td><td>Marcus Holm · EMP-188204</td></tr>
            <tr><td>Gross</td><td>€6,450</td></tr>
            <tr><td>Tax</td><td>€1,210</td></tr>
            <tr><td>Pension</td><td>€290</td></tr>
            <tr><td><strong>Net</strong></td><td><strong>€4,820</strong></td></tr>
          </tbody>
        </table>
      </article>
    `
    ),
};

function render() {
  const path = window.location.pathname.replace(/\/$/, "") || "/";
  const view = pages[path] || pages["/"];
  app.innerHTML = view();
}

document.addEventListener("click", (event) => {
  const link = event.target.closest("a[href^='/']");
  if (!link || event.metaKey || event.ctrlKey) return;
  event.preventDefault();
  history.pushState({}, "", link.getAttribute("href"));
  render();
});

window.addEventListener("popstate", render);
render();
