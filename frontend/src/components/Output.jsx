import React, { useState } from "react";
import NonCarousel from "./NonCarousel";
import Range from "./Range";

export default function Output() {

    return (
      <div id="output-page" className="container-fluid p-0">
      <Range />
      <NonCarousel />
      </div>
    );
  }
  
