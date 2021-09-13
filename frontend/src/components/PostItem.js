import React from "react";

function processDate(datetime) {
  return datetime.split("T")[0];
}

function PostItem(props) {
  return (
    <div className="col-lg-10 m-4">
      <div className="card p-4">
        <h2 className="card-title">
          <a className="card-link" href={`/post/${props.post.id}`}>{props.post.title}</a>
        </h2>
        <p className="card-text">{props.post.content}</p>
        <span className="card-text text-muted">Last update: { processDate(props.post.updated) } </span>
      </div>
      {/* <p className="">
        <span> by </span>
          <a href="#">{ props.post.author }</a>
      </p> */}
    </div>
  );
}

export default PostItem;
