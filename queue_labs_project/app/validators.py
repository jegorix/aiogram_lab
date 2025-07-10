
class Validators():
    
    @classmethod
    def fio_validate(cls, fio_from_user: str) -> bool:
        fio_list = fio_from_user.split()
        if len(fio_list) != 3:
            return False

        return True