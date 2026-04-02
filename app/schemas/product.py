from datetime import datetime

from pydantic import BaseModel, Field

from app.models.product import ProductStatus


class ProductBase(BaseModel):
	name: str = Field(..., min_length=1, max_length=255)
	price: float = Field(..., gt=0)
	details: str = Field(..., min_length=1)
	description: str | None = None
	category: str | None = None


class ProductCreate(ProductBase):
	pass


class ProductCreateResponse(BaseModel):
	status: str
	message: str


class ProductUpdate(BaseModel):
	name: str | None = None
	price: float | None = None
	details: str | None = None
	description: str | None = None
	category: str | None = None
	status: ProductStatus | None = None


class ProductRead(ProductBase):
	id: str
	status: ProductStatus
	owner_id: str
	created_at: datetime

	class Config:
		from_attributes = True

