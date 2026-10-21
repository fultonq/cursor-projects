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
        <article class="hr-card hr-kpi"><span>Headcount</span><strong>${HR_DIRECTORY.total.toLocaleString("en-US")}</strong></article>
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
              <tr><td>AMER</td><td>${HR_DIRECTORY.counts.AMER.toLocaleString("en-US")}</td><td>pg-amer</td></tr>
              <tr><td>EMEA</td><td>${HR_DIRECTORY.counts.EMEA.toLocaleString("en-US")}</td><td>pg-emea</td></tr>
              <tr><td>APAC</td><td>${HR_DIRECTORY.counts.APAC.toLocaleString("en-US")}</td><td>pg-apac</td></tr>
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
        <article class="hr-card hr-kpi"><span>Active employees</span><strong>${HR_DIRECTORY.total.toLocaleString("en-US")}</strong></article>
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
              <tr><td>AMER</td><td>${HR_DIRECTORY.counts.AMER.toLocaleString("en-US")}</td><td>hr_amer</td></tr>
              <tr><td>EMEA</td><td>${HR_DIRECTORY.counts.EMEA.toLocaleString("en-US")}</td><td>hr_emea</td></tr>
              <tr><td>APAC</td><td>${HR_DIRECTORY.counts.APAC.toLocaleString("en-US")}</td><td>hr_apac</td></tr>
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
      <div class="hr-row" style="justify-content: space-between">
        <div>
          <h1 class="hr-h1">Employee directory</h1>
          <p class="hr-sub" id="dir-sub">Loading workforce…</p>
        </div>
        <div class="hr-row">
          <button class="hr-btn ghost on" type="button" id="dir-view-table">Table</button>
          <button class="hr-btn ghost" type="button" id="dir-view-grid">Grid</button>
          <button class="hr-btn ghost" type="button" id="dir-export">Export page</button>
        </div>
      </div>
      <div class="hr-kpis" id="dir-kpis"></div>
      <div class="hr-row dir-filters">
        <input class="hr-field" id="dir-q" placeholder="Search name, ID, email, title" style="max-width: 280px; margin: 0" />
        <select class="hr-field dir-select" id="dir-region"><option value="">All regions</option><option>AMER</option><option>EMEA</option><option>APAC</option></select>
        <select class="hr-field dir-select" id="dir-org"><option value="">All orgs</option></select>
        <select class="hr-field dir-select" id="dir-city"><option value="">All locations</option></select>
        <select class="hr-field dir-select" id="dir-status">
          <option value="">All statuses</option>
          <option>Active</option>
          <option>Leave</option>
          <option>Contractor</option>
        </select>
        <button class="hr-btn ghost" type="button" id="dir-reset">Reset</button>
      </div>
      <article class="hr-card dir-card">
        <div class="dir-head" id="dir-head">
          <span></span><span>Employee</span><span>Title</span><span>Org</span><span>Location</span><span>Region</span><span>Status</span>
        </div>
        <div class="dir-viewport" id="dir-viewport">
          <div id="dir-rows"></div>
        </div>
        <div class="dir-grid" id="dir-grid" hidden></div>
        <div class="dir-pager hr-row" id="dir-pager"></div>
        <p class="hr-sub" id="dir-foot" style="margin: 0.75rem 1rem 1rem"></p>
      </article>
      <div class="hr-modal" id="dir-modal" hidden>
        <div class="hr-modal-backdrop" data-close="1"></div>
        <div class="hr-modal-card" role="dialog" aria-modal="true" aria-labelledby="modal-name"></div>
      </div>
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

function statusPill(status) {
  const kind = status === "Active" ? "ok" : status === "Leave" ? "warn" : "";
  return `<span class="hr-pill ${kind}">${status}</span>`;
}

function photoTag(person, size) {
  return `<img class="dir-photo" width="${size}" height="${size}" alt="${person.name}" src="${person.photo}" data-initials="${person.initials}" onerror="this.outerHTML='<span class=dir-fallback>'+this.dataset.initials+'</span>'" />`;
}

function profileHref(id) {
  return `/admin/directory?id=${encodeURIComponent(id)}`;
}

function findEmployee(idOrName) {
  return HR_DIRECTORY.employees.find((item) => item.id === idOrName || item.name === idOrName);
}

function managerCell(name) {
  const manager = findEmployee(name);
  if (!manager) return name;
  return `<a class="dir-link" href="${profileHref(manager.id)}">${manager.name}</a>`;
}

function setProfileUrl(id) {
  const url = id ? profileHref(id) : "/admin/directory";
  if (`${location.pathname}${location.search}` !== url) {
    history.pushState({ profile: id || null }, "", url);
  }
}

function openProfile(person, { syncUrl = true } = {}) {
  const modal = document.getElementById("dir-modal");
  if (!modal) return;
  const card = modal.querySelector(".hr-modal-card");
  card.innerHTML = `
    <button class="hr-modal-x" type="button" data-close="1" aria-label="Close">×</button>
    <div class="hr-modal-hero">
      ${photoTag(person, 96)}
      <div>
        <h2 class="hr-h1" id="modal-name">${person.name}</h2>
        <p class="hr-sub">${person.title} · ${person.org}</p>
        <p class="hr-sub">${person.city} · ${person.region} shard</p>
      </div>
    </div>
    <table class="hr-table">
      <tbody>
        <tr><td>Employee ID</td><td>${person.id}</td></tr>
        <tr><td>Email</td><td><a class="dir-link" href="mailto:${person.email}">${person.email}</a></td></tr>
        <tr><td>Phone</td><td>${person.phone}</td></tr>
        <tr><td>Manager</td><td>${managerCell(person.manager)}</td></tr>
        <tr><td>Hired</td><td>${person.hired}</td></tr>
        <tr><td>Timezone</td><td>${person.timezone}</td></tr>
        <tr><td>Status</td><td>${statusPill(person.status)}</td></tr>
      </tbody>
    </table>
  `;
  modal.hidden = false;
  if (syncUrl) setProfileUrl(person.id);
}

function closeProfile({ syncUrl = true } = {}) {
  const modal = document.getElementById("dir-modal");
  if (!modal) return;
  modal.hidden = true;
  if (syncUrl && new URLSearchParams(location.search).get("id")) setProfileUrl(null);
}

function initDirectory() {
  const { employees, total, counts, cities, orgs } = HR_DIRECTORY;
  const q = document.getElementById("dir-q");
  const region = document.getElementById("dir-region");
  const org = document.getElementById("dir-org");
  const city = document.getElementById("dir-city");
  const status = document.getElementById("dir-status");
  const viewport = document.getElementById("dir-viewport");
  const rows = document.getElementById("dir-rows");
  const grid = document.getElementById("dir-grid");
  const pager = document.getElementById("dir-pager");
  const head = document.getElementById("dir-head");
  const modal = document.getElementById("dir-modal");
  const viewTable = document.getElementById("dir-view-table");
  const viewGrid = document.getElementById("dir-view-grid");
  orgs.forEach((name) => org.insertAdjacentHTML("beforeend", `<option>${name}</option>`));
  cities.forEach((name) => city.insertAdjacentHTML("beforeend", `<option>${name}</option>`));
  document.getElementById("dir-kpis").innerHTML = `
    <article class="hr-card hr-kpi"><span>Global</span><strong>${total.toLocaleString("en-US")}</strong></article>
    <article class="hr-card hr-kpi"><span>AMER</span><strong>${counts.AMER.toLocaleString("en-US")}</strong></article>
    <article class="hr-card hr-kpi"><span>EMEA</span><strong>${counts.EMEA.toLocaleString("en-US")}</strong></article>
    <article class="hr-card hr-kpi"><span>APAC</span><strong>${counts.APAC.toLocaleString("en-US")}</strong></article>
  `;

  const PAGE_SIZE = 100;
  let filtered = employees;
  let view = "table";
  let page = 0;

  function applyFilters() {
    const query = q.value.trim().toLowerCase();
    filtered = employees.filter((person) => {
      if (region.value && person.region !== region.value) return false;
      if (org.value && person.org !== org.value) return false;
      if (city.value && person.city !== city.value) return false;
      if (status.value && person.status !== status.value) return false;
      if (!query) return true;
      return `${person.name} ${person.id} ${person.email} ${person.title} ${person.org} ${person.last}`.toLowerCase().includes(query);
    });
    page = 0;
    viewport.scrollTop = 0;
    paint();
  }

  function resetFilters() {
    q.value = "";
    region.value = "";
    org.value = "";
    city.value = "";
    status.value = "";
    applyFilters();
  }

  function pageWindow() {
    const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
    page = Math.min(Math.max(0, page), pages - 1);
    const start = page * PAGE_SIZE;
    const end = Math.min(filtered.length, start + PAGE_SIZE);
    return { start, end, pages };
  }

  function paintPager({ start, end, pages }) {
    pager.innerHTML = `
      <button class="hr-btn ghost" type="button" data-page="first" ${page === 0 ? "disabled" : ""}>First</button>
      <button class="hr-btn ghost" type="button" data-page="-1" ${page === 0 ? "disabled" : ""}>Previous</button>
      <span class="hr-sub" style="margin:0">Page ${page + 1} of ${pages.toLocaleString("en-US")} · ${PAGE_SIZE} per page</span>
      <button class="hr-btn ghost" type="button" data-page="1" ${page >= pages - 1 ? "disabled" : ""}>Next</button>
      <button class="hr-btn ghost" type="button" data-page="last" ${page >= pages - 1 ? "disabled" : ""}>Last</button>
    `;
    const hint = view === "grid" ? "click a card" : "click a name or row";
    document.getElementById("dir-foot").textContent =
      `Showing ${filtered.length ? start + 1 : 0}–${end} of ${filtered.length.toLocaleString("en-US")} · ${PAGE_SIZE} loaded · ${hint}`;
  }

  function setView(next) {
    view = next;
    viewTable.classList.toggle("on", view === "table");
    viewGrid.classList.toggle("on", view === "grid");
    head.hidden = view !== "table";
    viewport.hidden = view !== "table";
    grid.hidden = view !== "grid";
    paint();
  }

  function paintTable() {
    const { start, end, pages } = pageWindow();
    rows.innerHTML = filtered
      .slice(start, end)
      .map(
        (person) => `
      <a class="dir-row" href="${profileHref(person.id)}">
        ${photoTag(person, 40)}
        <span><strong class="dir-link">${person.name}</strong><small>${person.id}</small></span>
        <span>${person.title}</span>
        <span>${person.org}</span>
        <span>${person.city}</span>
        <span>${person.region}</span>
        <span>${statusPill(person.status)}</span>
      </a>`
      )
      .join("");
    paintPager({ start, end, pages });
  }

  function paintGrid() {
    const { start, end, pages } = pageWindow();
    grid.innerHTML = filtered
      .slice(start, end)
      .map(
        (person) => `
      <a class="dir-person" href="${profileHref(person.id)}">
        ${photoTag(person, 88)}
        <strong class="dir-link">${person.name}</strong>
        <small>${person.title}</small>
        <small>${person.city} · ${person.region}</small>
        ${statusPill(person.status)}
      </a>`
      )
      .join("");
    paintPager({ start, end, pages });
  }

  function paint() {
    document.getElementById("dir-sub").textContent =
      `${total.toLocaleString("en-US")} employees globally · 100 per page · photos · hot-linked profiles`;
    if (view === "grid") paintGrid();
    else paintTable();
  }

  [q, region, org, city, status].forEach((el) => el.addEventListener("input", applyFilters));
  document.getElementById("dir-reset").addEventListener("click", resetFilters);
  viewTable.addEventListener("click", () => setView("table"));
  viewGrid.addEventListener("click", () => setView("grid"));
  pager.addEventListener("click", (event) => {
    const action = event.target.closest("[data-page]")?.dataset.page;
    if (!action) return;
    const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
    if (action === "first") page = 0;
    else if (action === "last") page = pages - 1;
    else page += Number(action);
    viewport.scrollTop = 0;
    paint();
  });
  modal.addEventListener("click", (event) => {
    if (event.target.closest("[data-close]")) closeProfile();
  });
  if (!window.__hrEscBound) {
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeProfile();
    });
    window.__hrEscBound = true;
  }
  document.getElementById("dir-export").addEventListener("click", () => {
    const header = "id,name,title,org,city,region,status,email\n";
    const { start, end } = pageWindow();
    const body = filtered
      .slice(start, end)
      .map((person) => [person.id, person.name, person.title, person.org, person.city, person.region, person.status, person.email].join(","))
      .join("\n");
    const blob = new Blob([header + body], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    Object.assign(document.createElement("a"), { href: url, download: "directory-page.csv" }).click();
    URL.revokeObjectURL(url);
  });
  applyFilters();
  const selected = new URLSearchParams(window.location.search).get("id");
  if (selected) {
    const person = findEmployee(selected);
    if (person) openProfile(person, { syncUrl: false });
  }
}

function render() {
  const path = window.location.pathname.replace(/\/$/, "") || "/";
  const view = pages[path] || pages["/"];
  app.innerHTML = view();
  if (path === "/admin/directory") initDirectory();
}

document.addEventListener("click", (event) => {
  const link = event.target.closest("a[href^='/']");
  if (!link || event.metaKey || event.ctrlKey) return;
  const href = link.getAttribute("href");
  const next = new URL(href, window.location.origin);
  const here = window.location.pathname.replace(/\/$/, "") || "/";
  const there = next.pathname.replace(/\/$/, "") || "/";
  const profileId = next.searchParams.get("id");
  if (here === "/admin/directory" && there === "/admin/directory" && profileId) {
    event.preventDefault();
    const person = findEmployee(profileId);
    if (person) openProfile(person);
    return;
  }
  event.preventDefault();
  history.pushState({}, "", href);
  render();
});

window.addEventListener("popstate", render);
render();
