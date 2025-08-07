from dataclasses import asdict

from sqlalchemy import select

from models import User


def test_deve_criar_user_no_banco_de_dados(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            name='Carlos Eduardo', email='carlos@email.com', password='1234'
        )
        session.add(new_user)
        session.commit()
    result = session.scalar(select(User).where(User.email == 'carlos@email.com'))
    assert asdict(result) == {
        'id': 1,
        'name': 'Carlos Eduardo',
        'email': 'carlos@email.com',
        'password': '1234',
        'created_at': time,
    }
