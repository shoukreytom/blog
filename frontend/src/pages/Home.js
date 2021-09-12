import React from "react";
import { useCookies } from "react-cookie";
import Header from "../components/Header";
import Posts from "../components/Posts";

function Home() {
  const [cookies] = useCookies([]);
  if (cookies) {
    return (
      <div>
        <Header />
        <Posts token={cookies.token} />
      </div>
    );
  } else {
    return (
      <div>
        <Header />
      </div>
    );
  }
}

export default Home;
