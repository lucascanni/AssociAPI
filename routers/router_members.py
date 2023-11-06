from fastapi import APIRouter, Depends, HTTPException, status
from classes.schemas_dto import Member, MemberCreate
import uuid
from typing import List
from database.firebase import db
from routers.router_auth import get_current_user
from routers.router_stripe import increment_stripe

router = APIRouter(
    prefix='/members',
    tags=['members']
)

@router.get('', response_model=List[Member])
async def get_all_members(user_data: int= Depends(get_current_user)):
    firebase_members = db.child('users').child(user_data['uid']).child("members").get(user_data['idToken']).val()
    resultArray = [value for value in firebase_members.values()]
    return resultArray

@router.post('', response_model=Member, status_code=201)
async def create_member(member: MemberCreate, user_data: int= Depends(get_current_user)):
    generatedId = str(uuid.uuid4())
    newMember = Member(id= generatedId, **member.model_dump())
    # increment_stripe(user_data['uid'])
    return db.child('users').child(user_data['uid']).child("members").child(generatedId).set(newMember.model_dump(), token=user_data['idToken'])

@router.get('/{id}', response_model=Member)
async def get_member_by_id(id: str, user_data: int= Depends(get_current_user)):
    return db.child('users').child(user_data['uid']).child("members").child(id).get(user_data['idToken']).val()

@router.patch('/{id}', response_model=Member)
async def update_member(id: str, member: MemberCreate, user_data: int= Depends(get_current_user)):
    updatedMember = Member(id= id, **member.model_dump())
    return db.child('users').child(user_data['uid']).child("members").child(id).update(updatedMember.model_dump(), token=user_data['idToken'])

@router.delete('/{id}', response_model=Member)
async def delete_member(id: str, user_data: int= Depends(get_current_user)):
    deleteMember = db.child('users').child(user_data['uid']).child("members").child(id).get(user_data['idToken']).val()
    db.child('users').child(user_data['uid']).child("members").child(id).remove(token=user_data['idToken'])
    return deleteMember