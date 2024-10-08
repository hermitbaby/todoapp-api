from typing import Optional, List
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from beanie import Document, PydanticObjectId

import uuid

class UserSubscription(Document):
    userName: str
    subscribedLists: Optional[List[PydanticObjectId]] = None 

    createdDate: Optional[datetime] = None
    updatedDate: Optional[datetime] = None

class CreateUpdateUserSubscription(BaseModel):
    userName: str
    subscribedLists: List[PydanticObjectId]


class TodoList(Document):
    name: str
    description: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedDate: Optional[datetime] = None


class CreateUpdateTodoList(BaseModel):
    name: str
    description: Optional[str] = None


class TodoState(Enum):
    TODO = "todo"
    INPROGRESS = "inprogress"
    DONE = "done"

class TodoItem(Document):
    listId: PydanticObjectId
    name: str
    description: Optional[str] = None
    state: Optional[TodoState] = None
    dueDate: Optional[datetime] = None
    completedDate: Optional[datetime] = None
    createdDate: Optional[datetime] = None
    updatedDate: Optional[datetime] = None


class CreateUpdateTodoItem(BaseModel):
    name: str
    description: Optional[str] = None
    state: Optional[TodoState] = None
    dueDate: Optional[datetime] = None
    completedDate: Optional[datetime] = None

__beanie_models__ = [TodoList, TodoItem, UserSubscription]

