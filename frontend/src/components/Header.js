import React from "react";
import { useCookies } from "react-cookie";

function RightNavList(props) {
  if (!props.token) {
    return (
      <ul className="navbar-nav me-auto mb-2 mb-lg-0 d-flex">
        <li className="nav-item">
          <a className="nav-link mx-4" href="/login">
            Login
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link mx-4" href="/signup">
            Sign Up
          </a>
        </li>
      </ul>
    );
  } else {
    return (
      <ul className="navbar-nav me-auto mb-2 mb-lg-0 d-flex">
        <li className="nav-item">
          <a className="nav-link mx-4" href="/new">
            New Post
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link mx-4" href="/profile">
            Profile
          </a>
        </li>
      </ul>
    );
  }
}

function Header() {
  const [cookies, ] = useCookies([]);
  var token = "";
  if (cookies) token = cookies.token;
  return (
    <header>
      <nav className="navbar navbar-expand-md navbar-light bg-light border-bottom">
        <div className="container-fluid">
          <a className="navbar-brand mx-5" href="/">
            BlogDevPost
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <a className="nav-link mx-4" href="/">
                  Home
                </a>
              </li>
            </ul>
            <RightNavList token={token} />
          </div>
        </div>
      </nav>
    </header>
  );
}

export default Header;
