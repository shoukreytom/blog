import React, { useState } from "react";
import $ from "jquery";
import { Redirect } from "react-router";
import { useCookies } from "react-cookie";

function NewPostContent() {
  const [cookies, ] = useCookies([]);
  const HOST = "https://djangoblogdemo.herokuapp.com/";
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  // const [coverPhoto, setCoverPhoto] = useState("");
  const [created, setCreated] = useState(false);
  const submitPost = (status) => {
    if (title && content) {
      const postData = {title: title, content: content, status: status}
      // if(coverPhoto) {
      //   // postData["cover_photo"] = coverPhoto;
      //   console.log(coverPhoto);
      // }
      $.ajax({
        url: `${HOST}api/v1/posts/`,
        type: "post",
        data: postData,
        headers: {'Authorization': `Token ${cookies.token}` },
        success: function (result) {
          setCreated(true);
        },
        error: function (error) {
          console.log(error);
        },
      });
    }
  };
  const publish = (e) => {
      e.preventDefault();
      submitPost("published");
  }
  const save = (e) => {
      e.preventDefault();
      submitPost("draft");
  }
  if (created) {
    return <Redirect exact from="/new" to="/" />;
  }
  return (
    <div className="d-flex col justify-content-center text-center py-5">
      <form method="POST">
        <fieldset>
          <legend className="py-4 fw-bold">New post</legend>
          <div className="form-group py-2 w-100">
            <label htmlFor="title" className="form-label">Title<sup>*</sup></label>
            <input
              type="text"
              name="title"
              id="title"
              className="form-control"
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Title"
              required
            />
          </div>
          <div className="form-group py-2">
            <label htmlFor="content" className="form-label">Content *</label>
            <textarea
              name="content"
              id="content"
              className="form-control"
              placeholder="Content"
              onChange={(e) => setContent(e.target.value)}
              rows="15"
              required
            ></textarea>
          </div>
          {/* <div className="form-group py-2">
            <label htmlFor="cover-photo" className="form-label">Cover photo</label>
            <input
              type="file"
              name="cover_photo"
              className="form-control"
              onChange={(e) => setCoverPhoto(e.target.files)}
            />
          </div> */}
        </fieldset>
        <button className="btn btn-primary fw-bold my-4 mx-2" onClick={publish}>
          Publish
        </button>
        <button className="btn btn-primary fw-bold my-4 mx-2" onClick={save}>
          Save
        </button>
      </form>
    </div>
  );
}

export default NewPostContent;
