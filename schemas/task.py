from typing import Optional, Literal
from pydantic import Field, BaseModel


class CreateTasks(BaseModel): # Model to create a task include field to control what user passes and optional for optional inputs and Literal for specific inputs
    id: Optional[int] = Field(default=None, gt=0, description="Auto Generated ID")
    title: str = Field(min_length=1,max_length=15)
    description: Optional[str] = Field(min_length=2, max_length=30, default=None)
    completed: bool = False
    status: Literal["todo", "in-progress", "completed"] = Field(default="todo")
    priority: Literal["low", "medium", "high"] = Field(default="medium")

class ViewTasks(BaseModel): # Model to View the task we also specify the data type to control user input
    id: int
    title: str
    status: str

