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
    const key = `Token ${this.props.token}`;
    fetch(`${HOST}api/v1/posts/`, {
      method: "get",
      headers: { Authorization: key },
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
            <PostItem key={item.id} post={item} />
          ))}
        </div>
      );
    }
  }
}

export default Posts;
