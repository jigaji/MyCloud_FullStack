import axios from 'axios';
import Cookies from "js-cookie";


export const authToken =  Cookies.get("access_token");
console.log(authToken)


const apiInstance = axios.create({

    baseURL: 'http://127.0.0.1:8000/api/',

});

apiInstance.interceptors.request.use(
    (config) => {
      const token = Cookies.get("access_token");;
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

export default apiInstance;
