import type { Account } from "./types";

export const SAMPLE_ACCOUNTS: Account[] = [
  { id: "acc-1", company: "Nimbus Labs", industry: "saas", employees: 400, region: "north america", tech_stack: ["Kubernetes", "Snowflake"], signals: ["hiring engineers", "raised Series B"] },
  { id: "acc-2", company: "FinEdge", industry: "fintech", employees: 1200, region: "europe", tech_stack: ["Kafka"], signals: ["scaling rapidly"] },
  { id: "acc-13", company: "GreenFields Agtech", industry: "agriculture", employees: 500, region: "north america", tech_stack: [], signals: ["raised Series C"] },
];
