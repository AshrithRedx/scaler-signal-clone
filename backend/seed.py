from app.db.database import SessionLocal
from app.models.user import User
from app.models.conversation import Conversation
from app.models.conversation_member import ConversationMember
from app.models.message import Message


db = SessionLocal()


def get_user(username: str):
    return db.query(User).filter(User.username == username).first()


def get_conversation(name: str):
    return (
        db.query(Conversation)
        .filter(Conversation.name == name)
        .first()
    )


def create_user_if_not_exists(
    username: str,
    phone: str,
    display_name: str,
    avatar: str | None = None,
):
    existing = get_user(username)

    if existing:
        return existing

    user = User(
        username=username,
        phone_number=phone,
        display_name=display_name,
        avatar_url=avatar,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

USERS = [
    {
        "username": "kaelen",
        "phone": "9000000001",
        "display_name": "Kaelen Frost",
    },
    {
        "username": "lyra",
        "phone": "9000000002",
        "display_name": "Lyra Quinn",
    },
    {
        "username": "orion",
        "phone": "9000000003",
        "display_name": "Orion Vale",
    },
    {
        "username": "nyra",
        "phone": "9000000004",
        "display_name": "Nyra Solis",
    },
    {
        "username": "zephyr",
        "phone": "9000000005",
        "display_name": "Zephyr Knox",
    },
    {
        "username": "aeris",
        "phone": "9000000006",
        "display_name": "Aeris Rowan",
    },
    {
        "username": "kaia",
        "phone": "9000000007",
        "display_name": "Kaia Mercer",
    },
    {
        "username": "noctis",
        "phone": "9000000008",
        "display_name": "Noctis Hale",
    },
]


def seed_users():

    users = {}

    for user in USERS:

        created = create_user_if_not_exists(
            username=user["username"],
            phone=user["phone"],
            display_name=user["display_name"],
        )

        users[user["username"]] = created

    return users

def conversation_exists(name: str | None, created_by: str):

    return (
        db.query(Conversation)
        .filter(
            Conversation.name == name,
            Conversation.created_by == created_by,
        )
        .first()
    )


def create_conversation_if_not_exists(
    *,
    is_group: bool,
    name: str | None,
    created_by,
    members,
):

    existing = conversation_exists(
        name,
        created_by.id,
    )

    if existing:
        return existing

    conversation = Conversation(
        is_group=is_group,
        name=name,
        avatar_url=None,
        created_by=created_by.id,
    )

    db.add(conversation)
    db.flush()

    for member in members:

        db.add(
            ConversationMember(
                conversation_id=conversation.id,
                user_id=member.id,
                is_admin=(member.id == created_by.id),
            )
        )

    db.commit()
    db.refresh(conversation)

    return conversation

def seed_conversations(users):

    conversations = {}

    conversations["kaelen_lyra"] = create_conversation_if_not_exists(
        is_group=False,
        name=None,
        created_by=users["kaelen"],
        members=[
            users["kaelen"],
            users["lyra"],
        ],
    )

    conversations["lyra_orion"] = create_conversation_if_not_exists(
        is_group=False,
        name=None,
        created_by=users["lyra"],
        members=[
            users["lyra"],
            users["orion"],
        ],
    )

    conversations["kaia_zephyr"] = create_conversation_if_not_exists(
        is_group=False,
        name=None,
        created_by=users["kaia"],
        members=[
            users["kaia"],
            users["zephyr"],
        ],
    )

    conversations["nyra_aeris"] = create_conversation_if_not_exists(
        is_group=False,
        name=None,
        created_by=users["nyra"],
        members=[
            users["nyra"],
            users["aeris"],
        ],
    )

    conversations["core_engineers"] = create_conversation_if_not_exists(
        is_group=True,
        name="Core Engineers",
        created_by=users["kaelen"],
        members=[
            users["kaelen"],
            users["lyra"],
            users["orion"],
            users["zephyr"],
        ],
    )

    conversations["late_debuggers"] = create_conversation_if_not_exists(
        is_group=True,
        name="Late Night Debuggers",
        created_by=users["noctis"],
        members=[
            users["noctis"],
            users["kaia"],
            users["nyra"],
            users["aeris"],
        ],
    )

    return conversations

def add_message(conversation, sender, content):

    message = Message(
        conversation_id=conversation.id,
        sender_id=sender.id,
        content=content,
        status="sent",
    )

    db.add(message)

def seed_messages(users, conversations):

    if db.query(Message).count() > 0:
        return

    c = conversations

    add_message(c["kaelen_lyra"], users["kaelen"], "Did the authentication flow finally pass?")
    add_message(c["kaelen_lyra"], users["lyra"], "Yep. Swagger tests all passed.")
    add_message(c["kaelen_lyra"], users["kaelen"], "Perfect. Moving to the frontend next.")

    add_message(c["lyra_orion"], users["orion"], "Can you review my API routes?")
    add_message(c["lyra_orion"], users["lyra"], "Already looking at them.")
    add_message(c["lyra_orion"], users["orion"], "Awesome.")

    add_message(c["kaia_zephyr"], users["kaia"], "Coffee before standup?")
    add_message(c["kaia_zephyr"], users["zephyr"], "Always ☕")

    add_message(c["nyra_aeris"], users["nyra"], "Finished your assignment?")
    add_message(c["nyra_aeris"], users["aeris"], "Almost. WebSockets left.")

    add_message(c["core_engineers"], users["kaelen"], "Morning everyone!")
    add_message(c["core_engineers"], users["lyra"], "Morning 👋")
    add_message(c["core_engineers"], users["orion"], "Backend is green.")
    add_message(c["core_engineers"], users["zephyr"], "Frontend next.")

    add_message(c["late_debuggers"], users["noctis"], "Who's still awake?")
    add_message(c["late_debuggers"], users["kaia"], "Still debugging 😂")
    add_message(c["late_debuggers"], users["nyra"], "Same here.")
    add_message(c["late_debuggers"], users["aeris"], "Almost there!")

    db.commit()

def main():

    users = seed_users()

    conversations = seed_conversations(users)

    seed_messages(users, conversations)

    print("Database seeded successfully!")


if __name__ == "__main__":
    main()
