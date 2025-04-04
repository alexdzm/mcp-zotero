from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ZoteroCreator(BaseModel):
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    name: Optional[str] = None
    creator_type: Optional[str] = Field(None, alias="creatorType")

    class Config:
        populate_by_name = True


class ZoteroTag(BaseModel):
    tag: str
    type: Optional[int] = None


class ZoteroItemData(BaseModel):
    key: Optional[str] = None
    version: Optional[int] = None
    item_type: Optional[str] = Field(None, alias="itemType")
    title: Optional[str] = None
    creators: Optional[List[ZoteroCreator]] = None
    abstract_note: Optional[str] = Field(None, alias="abstractNote")
    date: Optional[str] = None
    date_added: Optional[str] = Field(None, alias="dateAdded")
    date_modified: Optional[str] = Field(None, alias="dateModified")
    doi: Optional[str] = Field(None, alias="DOI") 
    url: Optional[str] = None
    tags: Optional[List[ZoteroTag]] = None
    collections: Optional[List[str]] = None
    notes: Optional[List[Any]] = None
    publication_title: Optional[str] = Field(None, alias="publicationTitle")
    parent_collection: Optional[str] = Field(None, alias="parentCollection")
    num_items: Optional[int] = Field(None, alias="numItems")
    name: Optional[str] = None

    class Config:
        populate_by_name = True


class ZoteroLibrary(BaseModel):
    type: str
    id: int
    name: str


class ZoteroLink(BaseModel):
    href: str
    type: str


class ZoteroLinks(BaseModel):
    self: ZoteroLink
    alternate: ZoteroLink


class ZoteroMeta(BaseModel):
    num_items: Optional[int] = Field(None, alias="numItems")
    num_collections: Optional[int] = Field(None, alias="numCollections")

    class Config:
        populate_by_name = True


class ZoteroItem(BaseModel):
    key: str
    version: int
    library: ZoteroLibrary
    links: ZoteroLinks
    meta: ZoteroMeta
    data: ZoteroItemData

    class Config:
        populate_by_name = True 