(() => {
  const FIRST_F = [
    "Priya", "Amelia", "Leila", "Sofia", "Nora", "Mia", "Hannah", "Aisha", "Elena", "Yuki",
    "Fatima", "Ingrid", "Chloe", "Mei", "Lucia", "Anya", "Sara", "Camila", "Hana", "Freya",
    "Zara", "Isabelle", "Nia", "Priyanka", "Olivia", "Emma", "Ava", "Amara", "Lina", "Noor",
  ];
  const FIRST_M = [
    "Jonas", "Marcus", "Kenji", "Owen", "Arjun", "Diego", "Lukas", "Wei", "Noah", "Omar",
    "Andre", "Hiroshi", "Samuel", "Mateo", "Ibrahim", "Erik", "Raj", "Theo", "James", "Leo",
    "Daniel", "Carlos", "Minh", "Kwame", "Alexander", "Ben", "Hugo", "Soren", "Adrian", "Kai",
  ];
  const LAST = [
    "Nair", "Weber", "Holm", "Chen", "Haddad", "Alvarez", "Sato", "Ibrahim", "Blake", "Rossi",
    "Cole", "Mehta", "Kim", "Patel", "Nguyen", "Silva", "Johansson", "Dubois", "Kowalski", "Okafor",
    "Tanaka", "Berg", "Costa", "Murphy", "Khan", "Petrov", "Garcia", "Andersen", "Singh", "Moreau",
    "Nakamura", "Novak", "Fernandez", "Osei", "Williams", "Santos", "Lindqvist", "Park", "Rahman", "Bennett",
  ];
  const REGIONS = {
    AMER: {
      cities: ["New York", "Austin", "Chicago", "Toronto", "São Paulo", "Seattle", "Denver", "Mexico City"],
      tz: ["America/New_York", "America/Chicago", "America/Sao_Paulo", "America/Toronto", "America/Denver"],
    },
    EMEA: {
      cities: ["London", "Berlin", "Paris", "Stockholm", "Madrid", "Dubai", "Amsterdam", "Dublin", "Warsaw"],
      tz: ["Europe/London", "Europe/Berlin", "Europe/Paris", "Europe/Stockholm", "Asia/Dubai"],
    },
    APAC: {
      cities: ["Singapore", "Tokyo", "Sydney", "Bengaluru", "Seoul", "Hong Kong", "Melbourne", "Jakarta"],
      tz: ["Asia/Singapore", "Asia/Tokyo", "Australia/Sydney", "Asia/Kolkata", "Asia/Seoul"],
    },
  };
  const ORGS = [
    "People", "Product Engineering", "Platform", "Compensation", "Talent",
    "Finance", "Legal", "Sales", "Customer Success", "Operations", "Security", "Data",
  ];
  const TITLES = {
    People: ["People Partner", "HRBP", "People Ops Analyst", "Total Rewards Manager"],
    "Product Engineering": ["Staff Engineer", "Engineering Manager", "Software Engineer", "Principal Engineer", "QA Lead"],
    Platform: ["Staff Engineer", "SRE", "Platform Engineer", "Engineering Manager"],
    Compensation: ["Payroll Analyst", "Payroll Ops Lead", "Benefits Specialist"],
    Talent: ["Recruiter", "Sourcer", "Talent Partner"],
    Finance: ["Financial Analyst", "Controller", "FP&A Manager"],
    Legal: ["Counsel", "Compliance Officer", "Paralegal"],
    Sales: ["Account Executive", "Sales Manager", "Solutions Consultant"],
    "Customer Success": ["CSM", "Support Lead", "Onboarding Manager"],
    Operations: ["Ops Manager", "Workplace Lead", "Program Manager"],
    Security: ["Security Engineer", "GRC Analyst", "SOC Analyst"],
    Data: ["Data Engineer", "Analytics Engineer", "Data Scientist"],
  };

  function pick(list, n) {
    return list[n % list.length];
  }

  function seedEmployees(count) {
    const people = [
      { first: "Priya", last: "Nair", female: true, title: "People Partner", org: "People", city: "London", region: "EMEA", manager: "Amelia Chen" },
      { first: "Jonas", last: "Weber", female: false, title: "VP Engineering", org: "Product Engineering", city: "Berlin", region: "EMEA", manager: "Amelia Chen" },
      { first: "Marcus", last: "Holm", female: false, title: "Staff Engineer", org: "Platform", city: "Stockholm", region: "EMEA", manager: "Jonas Weber" },
      { first: "Amelia", last: "Chen", female: true, title: "Chief Executive Officer", org: "Office of the CEO", city: "London", region: "EMEA", manager: "—" },
      { first: "Leila", last: "Haddad", female: true, title: "Staff Engineer", org: "Platform", city: "Paris", region: "EMEA", manager: "Jonas Weber" },
      { first: "Sofia", last: "Alvarez", female: true, title: "Payroll Analyst", org: "Compensation", city: "Madrid", region: "EMEA", manager: "Priya Nair" },
      { first: "Kenji", last: "Sato", female: false, title: "Engineering Manager", org: "Product Engineering", city: "London", region: "EMEA", manager: "Jonas Weber" },
      { first: "Nora", last: "Ibrahim", female: true, title: "Recruiter", org: "Talent", city: "Dubai", region: "EMEA", manager: "Priya Nair" },
    ];

    const out = [];
    for (let i = 0; i < count; i += 1) {
      const named = people[i];
      const female = named ? named.female : i % 2 === 0;
      const first = named ? named.first : pick(female ? FIRST_F : FIRST_M, i * 7 + 3);
      const last = named ? named.last : pick(LAST, i * 13 + 5);
      const region = named ? named.region : ["AMER", "EMEA", "APAC"][i % 3 === 0 ? 0 : i % 3 === 1 ? 1 : 2];
      const meta = REGIONS[region];
      const org = named ? named.org : pick(ORGS, i * 3);
      const title = named ? named.title : pick(TITLES[org], i * 11);
      const city = named ? named.city : pick(meta.cities, i * 17);
      const id = `EMP-${String(100000 + i).padStart(6, "0")}`;
      const genderPath = female ? "women" : "men";
      const photoIdx = i % 99;
      out.push({
        id,
        first,
        last,
        name: `${first} ${last}`,
        email: `${first}.${last}${i > 40 ? i : ""}@aetherdynamics.com`.toLowerCase().replace(/\s+/g, ""),
        title,
        org,
        city,
        region,
        status: named ? "Active" : i % 47 === 0 ? "Leave" : i % 211 === 0 ? "Contractor" : "Active",
        manager: named ? named.manager : `${pick(FIRST_M, i + 2)} ${pick(LAST, i + 9)}`,
        hired: 2016 + (i % 10),
        timezone: pick(meta.tz, i),
        phone: `+${region === "AMER" ? "1" : region === "EMEA" ? "44" : "65"} 555 ${String(1000 + (i % 9000)).padStart(4, "0")}`,
        photo: `https://randomuser.me/api/portraits/${genderPath}/${photoIdx}.jpg`,
        initials: `${first[0]}${last[0]}`.toUpperCase(),
      });
    }
    return out;
  }

  const employees = seedEmployees(5280);
  const counts = employees.reduce((acc, person) => {
    acc[person.region] = (acc[person.region] || 0) + 1;
    return acc;
  }, {});

  window.HR_DIRECTORY = {
    employees,
    total: employees.length,
    counts,
    cities: [...new Set(employees.map((person) => person.city))].sort(),
    orgs: [...new Set(employees.map((person) => person.org))].sort(),
  };
})();
