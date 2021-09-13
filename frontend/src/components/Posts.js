import React from "react";
import PostItem from "./PostItem";

class Posts extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      posts: [],
    };
  }

  componentDidMount() {
    const HOST = "https://djangoblogdemo.herokuapp.com/";
    fetch(`${HOST}api/v1/posts/`, {
      method: "get",
    })
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            posts: result.results,
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      );
  }

  render() {
    const { error, isLoaded, posts } = this.state;
    if (error) {
      return <div>Error</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <div>
          {posts.map((item) => (
            <div className="row">
              <PostItem key={item.id} post={item} />
            </div>
          ))}
        </div>
      );
    }
  }
}

export default Posts;
