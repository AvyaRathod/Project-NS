import Carousel from "react-bootstrap/Carousel";
import React, { useState, useEffect } from "react";
import TimePicker from "react-time-picker";
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
  const [timeF, onChangeF] = useState("10:00:00");
  const [timeT, onChangeT] = useState("12:00:00");

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(epochTimeConverted(date.to + " " + timeT));
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
        <div className="from col-md-4 d-flex fs-4">
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
        </div>
        <TimePicker
          value={timeF}
          onChange={onChangeF}
        />

        <div className="col-md-4 to d-flex fs-4">
          <label for="to">To</label>
          <input
            type="date"
            className="form-control"
            id="to"
            name="to"
            onChange={onChangeT}
          />
        </div>
        <TimePicker
          value={timeT}
          onChange={onChangeT}
        />

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
                  src={`data:image/png;base64,${
                    queryItem["original_image"] || queryItem["segmented_image"]
                  }`}
                  alt="First slide"
                />
                <h3>Original</h3>
              </div>
              <div className="col-lg-6 p-0 text-center">
                <img
                  className="d-block cara-img"
                  src={`data:image/png;base64,${
                    queryItem["segmented_image"] || queryItem["original_image"]
                  }`}
                  alt="First slide"
                />
                <h3>Segmented</h3>
              </div>
              <div className="w-100 text-center nc-div">
                <h3 className="nuclei-counts bg-dark text-light rounded w-50">
                  Nuclei Count : {queryItem["adjusted_nuclei_count"]}
                </h3>
              </div>
            </div>
          </Carousel.Item>
        ))}
      </Carousel>
    </div>
  );
}
