import Carousel from "react-bootstrap/Carousel";
import React, { useState, useEffect } from "react";
import kicks from "./kicks.json";
import { initializeApp } from "firebase/app";
import {
  getFirestore,
  collection,
  where,
  getDocs,
  query,
  QuerySnapshot,
  orderBy,
} from "firebase/firestore";
import firebaseConfig from "./serviceAccountKey.json";

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const epochTimeConverted = (time) => {
  const date = new Date(time);
  const unixTimestamp = Math.floor(date.getTime() / 1000);
  return unixTimestamp;
};

export default function NonCarousel() {
  const dConstant = new Date();
  const [imageData, setImageData] = useState([kicks]);
  const [date, setDate] = useState({ to: dConstant.getTime(), from: 0 });

  const handleSubmit = async (event) => {
    event.preventDefault();
    const imagesRef = collection(db, "Images");
    const q = query(
      imagesRef,
      where("time", ">=", epochTimeConverted(date.from)),
      where("time", "<=", epochTimeConverted(date.to)),
      orderBy("time", "asc")
    );
    const querySnapshot = await getDocs(q);
    const temp = [];
    querySnapshot.forEach((doc) => {
      temp.push(doc.data());
    });
    setImageData(temp);
  };

  return (
    <div>
      <form
        className="date-form d-flex justify-content-center"
        method="post"
        action="#"
        onSubmit={handleSubmit}
      >
        <span className="from col-md-4 d-flex fs-4">
          <label for="from">From</label>
          <input
            type="date"
            className="form-control"
            id="from"
            name="From"
            onChange={(e) => {
              setDate({ from: e.target.value, to: date.to });
            }}
          />
        </span>
        <span className="col-md-4 to d-flex fs-4">
          <label for="to">To</label>
          <input
            type="date"
            className="form-control"
            id="to"
            name="to"
            onChange={(e) => {
              setDate({ to: e.target.value, from: date.from });
            }}
          />
        </span>
        <div>
          <input type="submit" className="btn btn-dark submit-btn-form"></input>
        </div>
      </form>
      <Carousel className="cara text-dark" interval={null}>
        {imageData.map((queryItem) => (
          <Carousel.Item>
            <div className="row text-center">
              <div className="col-lg-6 text-center p-0">
                <img
                  className="d-block cara-img"
                  src={`data:image/png;base64,${queryItem["segmented_image"]}`}
                  alt="First slide"
                />
                <h3>Original</h3>
                <p>Nuclei Count : {queryItem["nuclei_count"]}</p>
              </div>
              <div className="col-lg-6 p-0">
                <img
                  className="d-block cara-img"
                  src={`data:image/png;base64,${
                    queryItem["original_image"] || queryItem["segmented_image"]
                  }`}
                  alt="First slide"
                />
                <h3>Segmented</h3>
              </div>
            </div>
          </Carousel.Item>
        ))}
      </Carousel>
    </div>
  );
}
