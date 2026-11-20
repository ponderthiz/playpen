import axios from "axios";

const API_URL = "http://localhost:5000";

function register(uname, pword)  {
  return axios.post(API_URL+"/register", {
    uname,
    pword
  });
};

function getAdmin(){
    return axios.get(API_URL+"/admin");
};


const ApiService = {
    register,
    getAdmin
}


export default ApiService
