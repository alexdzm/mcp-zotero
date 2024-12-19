export interface ZoteroCreator {
  firstName?: string;
  lastName?: string;
  name?: string;
  creatorType?: string;
}

export interface ZoteroTag {
  tag: string;
  type?: number;
}

export interface ZoteroItemData {
  key?: string;
  version?: number;
  itemType?: string;
  title?: string;
  creators?: ZoteroCreator[];
  abstractNote?: string;
  date?: string;
  dateAdded?: string;
  dateModified?: string;
  DOI?: string;
  url?: string;
  tags?: ZoteroTag[];
  collections?: string[];
  notes?: any[];
  publicationTitle?: string;
  parentCollection?: string;
  numItems?: number;
  name?: string;
}

export interface ZoteroItem {
  key: string;
  version: number;
  library: {
    type: string;
    id: number;
    name: string;
  };
  links: {
    self: {
      href: string;
      type: string;
    };
    alternate: {
      href: string;
      type: string;
    };
  };
  meta: {
    numItems?: number;
    numCollections?: number;
  };
  data: ZoteroItemData;
}

export interface ZoteroRequestConfig {
  body?: any;
  headers?: Record<string, string>;
  params?: any;
}

export interface ZoteroApiInterface {
  library(type: string, id: number | string): ZoteroApiInterface;
  collections(key?: string): ZoteroApiInterface;
  items(key?: string): ZoteroApiInterface;
  top(): ZoteroApiInterface;
  trash(): ZoteroApiInterface;
  get(config?: any): Promise<any>;
}

export interface ZoteroApi {
  (key?: string): ZoteroApiInterface;
}
