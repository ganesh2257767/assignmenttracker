from app.models import Task, UpVote, DownVote
from fastapi import HTTPException, status
from sqlmodel import select, func

class VoteManager:
    def __init__(self, this_vote_model, other_vote_model, this_vote_field, other_vote_field):
        self.this_vote_model = this_vote_model
        self.other_vote_model = other_vote_model
        self.this_vote_field: str = this_vote_field
        self.other_vote_field: str = other_vote_field

    def toggle_votes(self, vote, session, current_user):
        task = session.get(Task, vote.task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        this_vote = select(self.this_vote_model).where(
            (self.this_vote_model.user_id == current_user.id) & (self.this_vote_model.task_id == vote.task_id)
        )
        other_vote = select(self.other_vote_model).where(
            (self.other_vote_model.user_id == current_user.id) & (self.other_vote_model.task_id == vote.task_id)
        )
        this_vote_data = session.scalar(this_vote)
        other_vote_data = session.scalar(other_vote)

        if this_vote_data:
            session.delete(this_vote_data)
            message = f"User: {current_user.email} removed {self.this_vote_field.removesuffix('s')} from task: {vote.task_id}"
        else:
            data = self.this_vote_model(user_id=current_user.id, task_id=vote.task_id)
            session.add(data)
            message = f"User: {current_user.email} {self.this_vote_field.replace('s', 'd')} task: {vote.task_id}"

            if other_vote_data:
                session.delete(other_vote_data)
                message += f", {self.other_vote_field.removesuffix('s')} removed automatically"

        session.commit()
        VoteManager.update_upvote_downvote_count(task, session)
        return message

    @staticmethod
    def update_upvote_downvote_count(task, session):
        upvotes = session.exec(select(func.count(UpVote.task_id)).where(UpVote.task_id == task.id)).one_or_none()
        downvotes = session.exec(select(func.count(DownVote.task_id)).where(DownVote.task_id == task.id)).one()

        task.upvotes = upvotes
        task.downvotes = downvotes
        session.add(task)
        session.commit()
        session.refresh(task)




