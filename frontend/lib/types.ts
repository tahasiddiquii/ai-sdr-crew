export type Tier = "A" | "B" | "C" | "disqualified";
export type CampaignStatus = "disqualified" | "awaiting_approval" | "approved" | "rejected";

export interface Account {
  id: string;
  company: string;
  industry: string;
  employees: number;
  region: string;
  tech_stack: string[];
  signals: string[];
}

export interface Qualification {
  fit_score: number;
  tier: Tier;
  reasons: string[];
}

export interface Fact {
  id: string;
  field: string;
  text: string;
}

export interface Claim {
  text: string;
  fact_id: string | null;
}

export interface Campaign {
  account_id: string;
  company: string;
  status: CampaignStatus;
  qualification: Qualification;
  facts: Fact[];
  draft: { subject: string; claims: Claim[]; cta: string } | null;
  review: { grounded: boolean; ungrounded_claims: string[]; note: string } | null;
  needs_review: boolean;
  approval: { approver: string; approve: boolean } | null;
}
