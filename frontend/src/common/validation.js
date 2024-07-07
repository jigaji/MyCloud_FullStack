import * as Yup from 'yup';

const regx= {
    login: /^[a-zA-Z]{1}[a-z0-9]{3,20}$/,
    email: /^\S+@\S+\.\S+$/,
    password: /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.,/])[A-Za-z\d@$!%*?&.,]{6,}$/,
};

const login = Yup.string()
    .matches(regx.login, 'Login should start with letter, consist of letters and numbers, 4-20 characters')
    .required("Enter login")


const email = Yup.string()
    .matches(regx.email, "Format example@example.com")
    .required('Enter email');

const password =Yup.string()
    .matches(regx.password, 'Password should be at least 6 characters and consist of one uppercase letter, one numeric digit, and one special character')
    .required('Enter password');

const password2 = Yup.string()
    .oneOf([Yup.ref('password')], 'Password doesn`t match')
    .required('Confirm password');


export const schema = {
    custom: Yup.object().shape({
        login,
        email, 
        password, 
        password2,
    })
}

export const initialValues = {
    login: "",
    email: "",
    password: "",
    password2: "",
}