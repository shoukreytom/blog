import React from "react";
import Header from "../components/Header";
import Posts from "../components/Posts";
// import TopPostsSidebar from "../components/TopPostsSidebar";
// import { useCookies } from "react-cookie";

function Home() {
  // const [cookies] = useCookies([]);
  return (
    <div>
      <Header />
      <Posts />
      {/* <TopPostsSidebar /> */}
    </div>
  )
}

export default Home;
