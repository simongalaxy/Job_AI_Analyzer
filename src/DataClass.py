from pydantic import BaseModel, Field
from typing import List, Optional



class ExtractedJobInfo(BaseModel):
    id: Optional[str] = Field(default=None, description="job id")
    job_title: str = Field(description="job title")
    responsibilities: List[str] = Field(description="core responsibilities of the job")
    qualifications: List[str] = Field(description="core educational qualifications and certificates")
    experiences: List[str] = Field(description="required working expereiences")
    technical_skills: List[str] = Field(description="all the technical skills")
    soft_skills: List[str] = Field(description="all the soft skills")
    industry: Optional[str] = Field(default=None, description="industry of the company")
