import Carousel from 'react-bootstrap/Carousel';
import image from "./kicks.json"

export default function NonCarousel() {
  return (
    <div>
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
        </div>
        <div className='col-lg-6 p-0'>
        <img
          className="d-block cara-img"     
          src={`data:image/png;base64,${image['image']}`}
          alt="First slide"
        />
        <h3>Segmented</h3>
        </div>
      </div>
      </Carousel.Item>
      <Carousel.Item>
      <div className='row text-center'>
        <div className='col-lg-6 text-center p-0'>
        <img
          className="d-block cara-img"     
          src={`data:image/png;base64,${image['image']}`}
          alt="First slide"
        />
        </div>
        <div className='col-lg-6 p-0'>
        <img
          className="d-block cara-img" 
          src={`data:image/png;base64,${image['image']}`}
          alt="First slide"
        />
        </div>
      </div>
      </Carousel.Item>
      <Carousel.Item>
      <div className='row text-center'>
        <div className='col-lg-6 text-center p-0'>
        <img
          className="d-block cara-img"     
          src={`data:image/png;base64,${image['image']}`}
          alt="First slide"
        />
        </div>
        <div className='col-lg-6 p-0'>
        <img
          className="d-block cara-img"     
          src={`data:image/png;base64,${image['image']}`}
          alt="First slide"
        />
        </div>
      </div>
      </Carousel.Item>
    </Carousel>
    </div>
  );
}
