import React, { useState, useEffect } from "react";
import Modal from "react-modal";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Button, Card, Badge} from 'react-bootstrap';
class Sub{
  constructor(){
    this.name = [];
    this.image = [];
    this.last_on_sale = [];
    this.price = [];
    this.on_sale = [];
    this.status = "";
    this.buttontype = "";
    this.original_name = [];
  }
}
Modal.setAppElement("#root")
function SubCard({position}) {
    let[subData, setSub] = useState([])
    const [modalIsOpen, setModalIsOpen] = useState(false)
    let sub = new Sub();
    useEffect(()=>{
        fetch('http://localhost:5000/onsale/')
        .then ((response) => response.json())
        .then((data) => setSub(data))
        .catch((error) => console.log(error))
      }, [])
    sub.name =  subData.map(pubsub => pubsub.name.replace("-", " "))
    sub.original_name = subData.map(pubsub => pubsub.name)
    sub.image = subData.map(pubsub => pubsub.image)
    sub.on_sale = subData.map(pubsub => pubsub.on_sale)
    sub.price = subData.map(pubsub => pubsub.price)
    sub.last_on_sale = subData.map(pubsub => pubsub.last_on_sale)
    if(sub.on_sale[position] === "False"){
      sub.status = "Not on sale"
      sub.buttontype = "danger"
    }else if(sub.on_sale[position] === "True"){
      sub.status = "Sale"
      sub.buttontype = "success"
    }
  return (
          <div>


            <Card>
              
              <Card.Body>
                <Card.Title>{sub.name[position]}</Card.Title>
                <Card.Img src = {sub.image[position]} />
                <Card.Text>
                  <Badge pill variant = {sub.buttontype} >
                      {sub.status}
                  </Badge>
                  <Button onClick={() => setModalIsOpen(true)}>
                      More Info
                  </Button>

                </Card.Text>
              </Card.Body>
             
            </Card>
            
            
            
            <Modal isOpen={modalIsOpen} onRequestClose={() => setModalIsOpen(false)}
            style={
              {
                overlay: {
                  backgroundColor: "gray"
                }
              }
            }>
            <center>
              <img src={sub.image[position]}></img>
              <p>Sub name: {sub.name[position]}</p>
              <p>Last time on sale: {sub.last_on_sale[position]}</p>
              <p>Price during sale: {sub.price[position]}</p>
              <p>Status: {sub.status}</p>
              <p>How to access {sub.name[position]} json:</p>
              <p>https://pubsub-api.dev/subs/?name={sub.original_name[position]}</p>
              <button onClick={() => setModalIsOpen(false)}>Close</button>
            </center>
            </Modal>
          </div>
  );
}

export default SubCard;
