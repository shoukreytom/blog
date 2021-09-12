import React, { useState } from "react";
import $ from "jquery";
import { Redirect } from "react-router";
import { useCookies } from "react-cookie";

function SignupContent() {
  const HOST = "https://djangoblogdemo.herokuapp.com/";
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [created, setCreated] = useState(false);
  const handle = (e) => {
    e.preventDefault();
    if (username && email && password && confirmPassword) {
      $.ajax({
        url: `${HOST}api/v1/users/auth/register/`,
        type: "post",
        data: {
          username: username,
          email: email,
          password: password,
          password2: confirmPassword,
        },
        success: function (result) {
          setCreated(true);
        },
        error: function (error) {
          console.log(error);
        },
      });
    }
  };
  if (created) {
    return <Redirect exact from="/signup" to="/login" />;
  }
  return (
    <div className="d-flex col justify-content-center text-center py-5">
      <form method="POST">
        <fieldset>
          <legend className="py-4 fw-bold">Sign Up</legend>
          <div className="form-group py-2">
            <input
              type="text"
              name="username"
              className="form-control"
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              required
            />
          </div>
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
          <div className="form-group py-2">
            <input
              type="password"
              name="password2"
              className="form-control"
              placeholder="Confirm password"
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
        </fieldset>
        <button className="btn btn-primary fw-bold my-4" onClick={handle}>
          Signup
        </button>
      </form>
    </div>
  );
}

export default SignupContent;
