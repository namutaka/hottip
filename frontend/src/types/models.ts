//
// models
//

import { DistributorType } from "../../types/globalTypes";

export interface Tip {
  id: string;
  title: string;
  text: string;
  enable: boolean;
}

export interface KeyValue {
  key: string;
  value: string | null;
}

export interface Distributor {
  id: string;
  type: DistributorType;
  schedule: string;
  tipsCount: number;
  attribute: KeyValue[];
}

export interface Channel {
  id: string;
  rawId: number | null;
  name: string;
  description: string;
  createdAt: any;
  updatedAt: any;
  tips: Tip[];
  distributors: Distributor[];
}
