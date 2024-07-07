import React, { useState } from "react";
import {  useNavigate } from "react-router-dom";
import { register } from "../utils/auth";
import { Formik, Form } from "formik";
import { initialValues, schema } from "../common/validation";
import LoadingIndicator from "../layouts/LoadingIndicator";
import {MDBBtn, MDBContainer, MDBRow, MDBCol, MDBCard, MDBCardBody, MDBInput} from 'mdb-react-ui-kit';
import 'mdb-react-ui-kit/dist/css/mdb.min.css';
import "@fortawesome/fontawesome-free/css/all.min.css";
import { object } from "yup";

function Register() {
    const [bioData, setBioData] = useState({full_name: "", username: "", email: "", password: "", password2: "" }, );
    const [isLoading, setIsLoading] = useState(false);
    const [errors, setErrors] = useState([])
    const [valid, setValid] = useState(true)
    const navigate = useNavigate();

    const handleBioDataChange = (event) => {
        setBioData({
            ...bioData,
            [event.target.name]: event.target.value,
        });
        console.log(bioData)
    };

    const resetForm = () => {
        setBioData({
            full_name: "",
            username: "",
            email: "",
            password: "",
            password2: "",

        });
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        let isvalid = true
        let validationErrors = {}
        if(bioData.username === "" || bioData.username === null) {
            isvalid=false
            validationErrors.username = "Login required"
        } else if(!/^[a-zA-Z]{1}[a-z0-9]{3,20}$/.test(bioData.username)) {
            isvalid=false
            validationErrors.username = "Login should start with letter, consist of letters and numbers, 4-20 characters"
        }
        if(bioData.email === "" || bioData.email === null) {
            isvalid=false
            validationErrors.email = "Password required"
        } else if(!/^\S+@\S+\.\S+$/.test(bioData.email)) {
            isvalid=false
            validationErrors.email = "Format example@example.com"
        }
        if(bioData.password === "" || bioData.password === null) {
            isvalid=false
            validationErrors.password = "Password required"
        } else if(!/^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.,/])[A-Za-z\d@$!%*?&.,]{6,}$/.test(bioData.password)) {
            isvalid=false
            validationErrors.username = "Password should be at least 6 characters and consist of one uppercase letter, one numeric digit, and one special character"
        }
        if(bioData.password !== bioData.password2) {
            isvalid=false
            validationErrors.password2 = "Confirm password doesn`t match"
        }
        setErrors(validationErrors)
        setValid(isvalid)

        if(Object.keys(validationErrors).length === 0) {
            
            const { error } = await register(bioData.full_name, bioData.username, bioData.email, bioData.password, bioData.password2, );
            if (error) {
                alert(JSON.stringify(error));
                resetForm();
            } else {
                alert("Registration is successfull")
                navigate("/login");
            }
            
            }
        setIsLoading(false);
        
    };

    return (

        
        <MDBContainer fluid>
            <form onSubmit={handleRegister} className="form-container">

                <MDBRow className='d-flex justify-content-center align-items-center h-100'>
                <MDBCol col='12'>

                    <MDBCard className='bg-dark text-white my-5 mx-auto' style={{borderRadius: '1rem', maxWidth: '400px'}}>
                    <MDBCardBody className='p-5 d-flex flex-column align-items-center mx-auto w-100'>
                    
                        <h2 className="fw-bold mb-2 text-uppercase">Registration</h2>
                        <p className="text-white-50 mb-5">Please enter your information!</p>    
                        
                        <MDBCol md='12'>
                            {
                                valid ? <></> : 
                                <></>
                            }

                           
                                    <MDBInput wrapperClass='mb-4' label='full name'  type='text'
                                        onChange={handleBioDataChange} value={bioData.full_name} id="full_name" className="form-control" name="full_name"/>
                                    
                                    <span className="text-danger"> {errors.username}</span>
                                    <MDBInput wrapperClass='mb-4' label='Login' type='text'
                                    onChange={handleBioDataChange} value={bioData.username} id="login" className="form-control" name="username" required=""/>
                                    
                                    
                                    
                                    <MDBInput wrapperClass='mb-4' label='Email' type='email'
                                    onChange={handleBioDataChange} value={bioData.email} id="email" className="form-control" name="email" required=""/>
                                    <span className="text-danger"> {errors.email}</span>

                                    <MDBInput wrapperClass='mb-4' label='Password' type='password'
                                    onChange={handleBioDataChange} value={bioData.password} id="password" className="form-control" name="password" placeholder="**************" required=""/>
                                    <span className="text-danger"> {errors.password}</span>

                                    <MDBInput wrapperClass='mb-4' label='Confirm password' type='password'
                                    onChange={handleBioDataChange} value={bioData.password2} id="password2" className="form-control" name="password2" placeholder="**************" required=""/>
                                    <span className="text-danger"> {errors.password2}</span>
                                
                                        {isLoading && <LoadingIndicator />}
                                        <MDBBtn outline className='mx-2 px-5' color='white' size='lg'>
                                        Register
                                        </MDBBtn>
                            
            
                            </MDBCol>
                    </MDBCardBody>
                    </MDBCard>
            
                </MDBCol>
                </MDBRow>
            </form>
        </MDBContainer>
    );
}

export default Register;