import React, { useState } from "react";
import ApiService from "../services/api-service";

function Register(){

    const [uname, setUsername] = useState("");
    const [pword, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [message, setMessage] = useState("");
    const [messageColor, setMessageColor] = useState("error");

    function onChangeUsername (event){
        setUsername(event.target.value);
    }
    function onChangePassword(event){
        setPassword(event.target.value);
    }
     function onChangeConfirm(event){
        setConfirm(event.target.value);
    }
    function onSubmit(event){
        event.preventDefault();
        if (uname === "") {

            setMessageColor("error");
            setMessage("Username is empty.");
            return;
        }
        if (pword === "") {

            setMessageColor("error");
            setMessage("Password is empty.");
            return;
        }
        if(confirm === ""){

            setMessageColor("error");
            setMessage("Confirm Password is empty.");
            return;
        }
        if(pword !== confirm){

           setMessageColor("error");
           setMessage("Both passwords must match.");
            return;
        }
        ApiService.register(uname, pword).then(
          (response) => {
            setMessageColor("success");
            setMessage(response.data.Message);
          },
          (error) => {
              setMessageColor("error");
              setMessage(error.toString());
          }
        );
    }

 return(
  <div id="card">
    <form  onSubmit={onSubmit}>
    <h2 >Register</h2>
    {message ? (<p className={messageColor}>{message}</p>):"" }
    <div>
      <label htmlFor="uname">Username</label>
      <input type="text" id="uname" value={uname} onChange={onChangeUsername} placeholder="Enter username..." />
    </div>
    <div>
      <label htmlFor="pword">Password</label>
      <input type="password" id="pword" value={pword} onChange={onChangePassword} placeholder="Enter password..." />
    </div>
    <div>
      <label htmlFor="confim">Confirm Password</label>
      <input type="password" id="confirm" value={confirm} onChange={onChangeConfirm}  placeholder="Confirm password..." />
    </div>

    <div>
      <button type="submit">Register</button>
    </div>
  </form>
  </div>
 )

}
export default Register;
