from firebase_admin import auth
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST


class Student:

    dept_list = {
        'bce': 'Biochemical Engineering',
        'bme': 'Biomedical Engineering',
        'cer': 'Ceramic Engineering',
        'che': 'Chemical Engineering',
        'chy': 'Chemistry',
        'civ': 'Civil Engineering',
        'cse': 'Computer Science and Engineering',
        'ece': 'Electronics Engineering',
        'eee': 'Electrical Engineering',
        'mat': 'Mathematics and Computing',
        'mec': 'Mechanical Engineering',
        'met': 'Metallurgical Engineering',
        'min': 'Mining Engineering',
        'mst': 'Materials Science and Technology',
        'phe': 'Pharmaceutical Engineering and Technology',
        'phy': 'Physics',
        'hss': 'Humanistic Studies'
    }

    roll_to_dept_list = {
        '01': 'bce',
        '02': 'bme',
        '03': 'cer',
        '04': 'che',
        '05': 'chy',
        '06': 'civ',
        '07': 'cse',
        '08': 'eee',
        '09': 'ece',
        '10': 'mec',
        '11': 'mst',
        '12': 'mat',
        '13': 'mec',
        '14': 'met',
        '15': 'min',
        '16': 'phe',
        '17': 'phy',
        '18': 'eee',
        '19': 'hss'
    }

    roll_to_course_list = {
        '1': 'Ph.D',
        '2': 'M.Tech',
        '3': 'IDD',
        '4': 'IDD',
        '5': 'B.Tech',
        '6': 'Post Doctoral Fellow'
    }

    @classmethod
    def get_department_code(cls, email):
        username = email.split('@')[0]
        dept_code = username.split('.')[-1][:3]
        return dept_code
    
    @classmethod
    def get_department(cls, email):
        dept_code = cls.get_department_code(email)
        return cls.dept_list[dept_code]
    
    @classmethod
    def get_year(cls, email):
        username = email.split('@')[0]
        year = username.split('.')[-1][3:]
        return '20' + year
    
    @classmethod
    def get_course(cls, roll_number):
        course = roll_number[4:5]
        return cls.roll_to_course_list[course]
    
    @classmethod
    def verify_email(cls, email):
        username = email.split('@')[0]
        domain = email.split('@')[1]
        if domain not in ['itbhu.ac.in', 'iitbhu.ac.in']:
            return False
        if '.' not in username:
            return False
        dept_code = cls.get_department_code(email)
        if dept_code not in cls.dept_list:
            return False
        return True

    @classmethod
    def verify_roll_number(cls, roll_number, email):
        year = '20' + roll_number[:2]
        dept = roll_number[2:4]
        dept_no = ''
        if dept not in cls.roll_to_dept_list:
            return False
        else:
            dept_code = cls.roll_to_dept_list[dept]
        course = roll_number[4:5]
        if year == cls.get_year(email) and dept_code == cls.get_department_code(email) and course in cls.roll_to_course_list:
            return True
        else:
            return False


class FirebaseAPI:

    @classmethod
    def verify_id_token(cls, id_token):
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except ValueError:
            raise ValidationError('Invalid Firebase ID Token.', HTTP_422_UNPROCESSABLE_ENTITY)
    
    @classmethod
    def get_name(cls, jwt):
        name = jwt.get('name', '')
        return name
    
    @classmethod
    def get_email(cls, jwt):
        email = jwt.get('email', '')
        return email
    
    @classmethod
    def delete_user_by_uid(cls, uid):
        auth.delete_user(uid)