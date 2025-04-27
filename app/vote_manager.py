from app.models import Post, UpVote, DownVote
from fastapi import HTTPException, status
from sqlmodel import select, func

class VoteManager:
    def __init__(self, this_vote_model, other_vote_model, this_vote_field, other_vote_field):
        self.this_vote_model = this_vote_model
        self.other_vote_model = other_vote_model
        self.this_vote_field: str = this_vote_field
        self.other_vote_field: str = other_vote_field

    def toggle_votes(self, vote, session, current_user):
        post = session.get(Post, vote.post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        this_vote = select(self.this_vote_model).where(
            (self.this_vote_model.user_id == current_user.id) & (self.this_vote_model.post_id == vote.post_id)
        )
        other_vote = select(self.other_vote_model).where(
            (self.other_vote_model.user_id == current_user.id) & (self.other_vote_model.post_id == vote.post_id)
        )
        this_vote_data = session.scalar(this_vote)
        other_vote_data = session.scalar(other_vote)

        if this_vote_data:
            session.delete(this_vote_data)
            message = f"User: {current_user.email} removed {self.this_vote_field.removesuffix('s')} from post: {vote.post_id}"
        else:
            data = self.this_vote_model(user_id=current_user.id, post_id=vote.post_id)
            session.add(data)
            message = f"User: {current_user.email} {self.this_vote_field.replace('s', 'd')} post: {vote.post_id}"

            if other_vote_data:
                session.delete(other_vote_data)
                message += f", {self.other_vote_field.removesuffix('s')} removed automatically"

        session.commit()
        VoteManager.update_upvote_downvote_count(post, session)
        return message

    @staticmethod
    def update_upvote_downvote_count(post, session):
        upvotes = session.exec(select(func.count(UpVote.post_id)).where(UpVote.post_id == post.id)).one_or_none()
        downvotes = session.exec(select(func.count(DownVote.post_id)).where(DownVote.post_id == post.id)).one()

        post.upvotes = upvotes
        post.downvotes = downvotes
        session.add(post)
        session.commit()
        session.refresh(post)




