from fastapi import APIRouter, Depends, HTTPException, status
from classes.schemas_dto import Member, MemberCreate
import uuid
from typing import List
from database.firebase import db

router = APIRouter(
    prefix='/members',
    tags=['members']
)

@router.get('', response_model=List[MemberCreate])
async def get_all_members():
    firebase_members = db.child("members").get().val()
    resultArray = [value for value in firebase_members.values()]
    return resultArray
    
    


@router.post('', response_model=MemberCreate, status_code=201)
async def create_member(member: MemberCreate):
    newMember = member.model_dump()
    return db.child("members").child(str(uuid.uuid4())).set(newMember)

@router.get('/{id}', response_model=MemberCreate)
async def get_member_by_id(id: str):
    memberById = db.child("members").child(id).get().val()
    return memberById

@router.put('/{id}', response_model=MemberCreate)
async def update_member(id: str, member: MemberCreate):
    db.child("members").child(id).update(member)
    return member

@router.delete('/{id}', response_model=MemberCreate)
async def delete_member(id: str):
    memberById = db.child("members").child(id).get().val()
    return {}