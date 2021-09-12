import React from "react";

function PostItem(props) {
  return (
    <div className="container my-4">
      <h1>
        <a href={`/post/${props.post.id}`}>{props.post.title}</a>
      </h1>
      <p>{props.post.content}</p>
    </div>
  );
}

export default PostItem;
