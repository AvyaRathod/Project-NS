import Carousel from "react-bootstrap/Carousel";
import React, { useState } from "react";
import kicks from "./kicks.json";
import { initializeApp } from "firebase/app";
import {
  getFirestore,
  collection,
  where,
  getDocs,
  query,
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
  const [date, setDate] = useState({ to: 0, from: 0 });
  const handleSubmit = async (event) => {
    event.preventDefault();
    const imagesRef = collection(db, "Images");
    const q = query(
      imagesRef,
      where("time", ">=", epochTimeConverted(date.from)),
      where("time", "<=", epochTimeConverted(date.to))
    );
    const querySnapshot = await getDocs(q);
    console.log(epochTimeConverted(date.to));
    querySnapshot.forEach((doc) => {
      console.log(doc.id, " => ", doc.data());
    });
  };
  return (
    <div>
<<<<<<< HEAD
      <form
        className="date-form d-flex justify-content-center"
        method="post"
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
=======
    <Carousel className='cara text-dark' interval={null}>
      <Carousel.Item>
      <div className='row text-center'>
        <div className='col-lg-6 text-center p-0'>
        <img
          className="d-block cara-img"     
          src={`data:image/png;base64,${image['image']}`}
          alt="First slide"
        />
        <h3>Original</h3>
>>>>>>> 3e111d1ea7ac14eb5078de24f2262ca2dfbbd533
        </div>
      </form>
      <Carousel className="cara text-dark" interval={null}>
        <Carousel.Item>
          <div className="row text-center">
            <div className="col-lg-6 text-center p-0">
              <img
                className="d-block cara-img"
                src={`data:image/png;base64,${kicks["image"]}`}
                alt="First slide"
              />
              <h3>Original</h3>
            </div>
            <div className="col-lg-6 p-0">
              <img
                className="d-block cara-img"
                src={`data:image/png;base64,${kicks["image"]}`}
                alt="First slide"
              />
              <h3>Segmented</h3>
            </div>
          </div>
        </Carousel.Item>
        <Carousel.Item>
          <div className="row text-center">
            <div className="col-lg-6 text-center p-0">
              <img
                className="d-block cara-img"
                src={`data:image/png;base64,${kicks["image"]}`}
                alt="First slide"
              />
            </div>
            <div className="col-lg-6 p-0">
              <img
                className="d-block cara-img"
                src={`data:image/png;base64,${kicks["image"]}`}
                alt="First slide"
              />
            </div>
          </div>
        </Carousel.Item>
        <Carousel.Item>
          <div className="row text-center">
            <div className="col-lg-6 text-center p-0">
              <img
                className="d-block cara-img"
                src={`data:image/png;base64,${kicks["image"]}`}
                alt="First slide"
              />
            </div>
            <div className="col-lg-6 p-0">
              <img
                className="d-block cara-img"
                src={`data:image/png;base64,${kicks["image"]}`}
                alt="First slide"
              />
            </div>
          </div>
        </Carousel.Item>
      </Carousel>
    </div>
  );
}
