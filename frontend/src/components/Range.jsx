export default function Range(){

    return(
        <form className='date-form d-flex justify-content-center'>
        <span className='from col-md-4 d-flex fs-4'>
        <label for="from">From</label>
      <input type="date" className="form-control" id="from" name="From" />
        </span>
        <span className='col-md-4 to d-flex fs-4'>
        <label for="to">To</label>
      <input type="date" className="form-control" id="to" name="to" />
        </span>
        <div>
        <input type="submit" className='btn btn-dark submit-btn-form'></input>
        </div>
        </form>
    )
}
