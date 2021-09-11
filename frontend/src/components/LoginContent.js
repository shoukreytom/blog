import React, { useState } from "react";
import $ from "jquery";
import { Redirect } from "react-router";
import { useCookies } from "react-cookie";

function LoginContent() {
  const HOST = "https://djangoblogdemo.herokuapp.com/"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");
  const [cookies, setCookie] = useCookies([])
  const handle = (e) => {
    e.preventDefault();
    if(email && password) {
      $.ajax({
        url: `${HOST}api/v1/users/auth/login/`,
        type: "post",
        data: {"email": email, "password": password},
        success: function(result) {
          setToken(result.token);
        },
        error: function(error) {
          console.log(error);
        }
      })
    }
  }
  if(token) {
    setCookie("token", token)
    return <Redirect exact from="/login" to="/" />
  }
  return (
    <div className="d-flex col justify-content-center text-center py-5">
      <form method="POST">
        <fieldset>
          <legend className="py-4 fw-bold">Login</legend>
          <div className="form-group py-2">
            <input
              type="email"
              name="email"
              className="form-control"
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              required
            />
          </div>
          <div className="form-group py-2">
            <input
              type="password"
              name="password"
              className="form-control"
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
        </fieldset>
        <button className="btn btn-primary fw-bold my-4" onClick={handle}>Login</button>
      </form>
    </div>
  );
}

export default LoginContent;
