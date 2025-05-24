from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from beanie import PydanticObjectId
from server.models.device import Device

router = APIRouter(prefix = "/devices", tags=["Devices"])

@router.get("/")
async def read_all_devices():
  return await Device.find_all().to_list()
