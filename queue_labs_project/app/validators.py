from string import ascii_letters

class Validators():
    S_RUS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя-'
    S_RUS_UPPER = S_RUS.upper()
    
    @classmethod
    def fio_validate(cls, fio_from_user: str) -> bool:
        
        if not isinstance(fio_from_user, str):
            return False
        
        fio_list = fio_from_user.split()
        if len(fio_list) != 3:
            return False
        
        letters = ascii_letters + cls.S_RUS + cls.S_RUS_UPPER
        
        for s in fio_list:
            if len(s) < 1:
                return False
            
            if len(s.strip(letters)) != 0:
                return False
        
        return True
    
    @classmethod
    def lab_number_validate(cls, user_number: str | int) -> bool | int:
        try:
            number = int(user_number)
        except ValueError:
            return False
        return number
    
    @classmethod
    def sub_group_validate(cls, user_group: str | int) -> bool | int:
        try:
            user_group_number = int(user_group)
        except ValueError:
            return False
            
        if user_group_number not in (1,2):
            return False
    
        return user_group_number
        

    @classmethod
    def github_link_validate(cls, github_link: str) -> bool | str:
        if not github_link.strip().startswith("https://github.com/"):
            return False
        return github_link

        