from app.models import UpVote, DownVote, User
from app.oauth2 import verify_and_get_current_user
from app.schemas import UpVoteCreate, DownVoteCreate, VoteResponse
from app.database import get_session
from fastapi import Depends, APIRouter, status
from sqlmodel import Session
from app.vote_manager import VoteManager

router = APIRouter(
    prefix="/vote",
    tags=['Voting']
)


@router.post("/up", status_code=status.HTTP_200_OK, response_model=VoteResponse)
def upvote(vote: UpVoteCreate, session: Session = Depends(get_session), current_user: User = Depends(verify_and_get_current_user)):
    vote_manager = VoteManager(UpVote, DownVote, "upvotes", "downvotes")
    message = vote_manager.toggle_votes(vote, session, current_user)
    return {
        "message": message
    }

@router.post("/down", status_code=status.HTTP_200_OK, response_model=VoteResponse)
def downvote(vote: DownVoteCreate, session: Session = Depends(get_session), current_user: User = Depends(verify_and_get_current_user)):
    vote_manager = VoteManager(DownVote, UpVote, "downvotes", "upvotes")
    message = vote_manager.toggle_votes(vote, session, current_user)
    return {
        "message": message
    }