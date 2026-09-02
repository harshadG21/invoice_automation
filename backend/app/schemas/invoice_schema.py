from datetime import date
from typing import Optional,Literal

from pydantic import BaseModel,Field

class VendorData(BaseModel):
    name:Optional[str] = None
    email:Optional[str] = None
    phone:Optional[str] = None
    address:Optional[str]=None
    gst_number:Optional[str]=None
    pan_number:Optional[str] = None

class FinancialData(BaseModel):
    subtotal :Optional[float] = None
    tax_amount : Optional[float] = None
    total_amount : Optional[float] = None
    currency : Optional[str] = None

class InvoiceData(BaseModel):
    document_type : Literal["invoice","not_an_invoice"]
    invoice_number:Optional[str] = None
    invoice_date:Optional[date] = None
    due_date:Optional[date]= None
    vendor : VendorData = Field(default_factory=VendorData)
    financial : FinancialData = Field(default_factory=FinancialData)

    