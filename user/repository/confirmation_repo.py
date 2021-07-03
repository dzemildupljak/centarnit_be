import datetime
from user.repository import user_repo
import msgpack
from sqlalchemy.orm.session import Session

from user.helpers.helpers import generate_ot_confirmation_code


def req_confirmation_generator(user_credentials: str, db: Session):
    load_items = []
    if '@' in user_credentials:
        new_user = user_repo.get_user_by_email(user_credentials, db)
    new_user = user_repo.get_user_by_username(user_credentials, db)

    try:
        with open('stream.msgpack', 'rb+') as f:
            load_items = [item for item in msgpack.Unpacker(f)]
    except:
        pass

    current_time = datetime.datetime.now()
    current_code = generate_ot_confirmation_code(current_time)
    for i in load_items:
        if new_user.email == i['email']:
            i['code'] = current_code
            with open('stream.msgpack', 'wb') as f:
                for i in load_items:
                    f.write(msgpack.packb(i))
            return current_code
    load_items.append(
        {
            'code': current_code,
            'email': new_user.email,
            'time': str(current_time)
        }
    )
    with open('stream.msgpack', 'wb') as f:
        for i in load_items:
            f.write(msgpack.packb(i))
    return current_code
