import React, { useState, useEffect } from "react";
import "./CSS/chat.css";

function Chatapp() {
  // add random cliend id by date time
  let username = localStorage.getItem("username");
  let reciever = localStorage.getItem("friend_id");
  let chat_id = localStorage.getItem("chat_id");
  const [clientId, setClientId] = useState(0);
  const [vpid, setVpid] = useState(0);

  const [websckt, setWebsckt] = useState();
  const [message, setMessage] = useState([]);
  const [messages, setMessages] = useState([]);
  const [vpSetting, setVpSetting] = useState([]);
  const [users, setUsers] = useState([]);
  const [itsyou, setItsyou] = useState("you");

  useEffect(() => {
    getAllUsers();
  }, []);

  const getAllUsers = () => {
    let token = localStorage.getItem("access_token");
    fetch("http://localhost:8000/userall", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setUsers(data.data);
      })
      .catch((err) => console.log(err));
  };

  const connectToWebsocket = (clientId) => {
    console.log(
      clientId +
        "-----------------------------------connection id from inside the function"
    );
    const url = "ws://localhost:8000/ws/" + clientId;
    const ws = new WebSocket(url);

    ws.onopen = (event) => {
      ws.send("Connect");
    };

    // recieve message every start page
    ws.onmessage = (e) => {
      const message = JSON.parse(e.data);
      setMessages([...messages, message]);
    };

    setWebsckt(ws);
    //clean up function when we close page
    return () => ws.close();
  };
  const sendMessage = () => {
    websckt.send(message);
    websckt.onmessage = (e) => {
      const message = JSON.parse(e.data);
      setMessages([...messages, message]);
      console.log(message, "message from send message");
      vpSetting.push(message);
      setVpSetting(vpSetting);
    };
    setMessage([]);
  };

  const handleUserchat = (e) => {
    username = e.target.innerText;
    let friendId = "";
    for (let i = 0; i < users.length; i++) {
      if (users[i].email === username) {
        friendId = users[i].id;
        break;
      }
    }

    fetch(`http://localhost:8000/chats/${friendId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.message == "Chat created successfully") {
          alert("Chat created successfully");
        }

        // from username remove @ and gmail.com
        username = username.replace("@gmail.com", "");
        username = username.toUpperCase();
        setItsyou(username);

        document.getElementById("chat-header-text").innerText = username;
        localStorage.setItem("chat_id", data.chat_id);
        localStorage.setItem("friend_id", friendId);
        setClientId(data.chat_id);
        connectToWebsocket(data.chat_id);

        fetch(`http://localhost:8000/messages/${data.chat_id}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
          .then((res) => res.json())
          .then((data) => {
            setVpSetting(data.data);
            setVpid(data.id);
          })
          .catch((err) => console.log(err));
      })
      .catch((err) => console.log(err));
    // chat-header-text
  };

  return (
    <div className="container">
      <h4>CHATSAPP</h4>
      <h2>Hello {username} </h2>
      <div className="main">
        <div className="user-container">
          <div className="headuser">
            <h1>You can chat with 🔽</h1>
          </div>
          <div className="user">
            {users.map((value, index) => {
              return (
                <div key={index} className="user-list">
                  <button className="user-button" onClick={handleUserchat}>
                    {value.email}
                  </button>
                </div>
              );
            })}
          </div>
        </div>
        <div className="chat-container">
          <div className="chat">
            <div className="chat-header">
              <p id="chat-header-text">Chat with your friends 😉</p>
            </div>
            {vpSetting ? (
              (console.log(vpid),
              vpSetting.map((value, index) => {
                console.log(value.sender_id == vpid);
                if (value.sender_id === vpid) {
                  return (
                    <div key={index} className="my-message-container">
                      <div className="my-message">
                        {/* <p className="client">client id : {clientId}</p> */}
                        <p className="message">
                          {" "}
                          <span className="itsmemsg">{value.message}</span>
                          <span className="itsme">me</span>{" "}
                        </p>
                      </div>
                    </div>
                  );
                } else {
                  return (
                    <div key={index} className="another-message-container">
                      <div className="another-message">
                        {/* <p className="client">client id : {clientId}</p> */}
                        <p className="message">
                          <span className="itsyou" id="itsyoushowing">
                            {itsyou}
                          </span>
                          <span className="itsyoumsg">{value.message}</span>
                        </p>
                      </div>
                    </div>
                  );
                }
              }))
            ) : (
              <p>No messages available.</p>
            )}
          </div>
          <div className="input-chat-container">
            <input
              className="input-chat"
              type="text"
              placeholder="Chat message ..."
              onChange={(e) => setMessage(e.target.value)}
              value={message}
            ></input>
            <button className="submit-chat" onClick={sendMessage}>
              Send
            </button>
          </div>
        </div>
        <div className="image-container">
          <div>
            <img
              src="https://www.freeiconspng.com/thumbs/profile-icon-png/am-a-19-year-old-multimedia-artist-student-from-manila--21.png"
              alt="chat"
            />
          </div>
          <h3 id="demoidshow">Demo@gmail.com</h3>
          <p id="demoidpara">My life my rules 😎 and njckasdn  cjd janjkdnjn djnjaknsjdn jnskjdnjdnj  dnjdjknjkdnjn</p>
          <div className="media">
            <h4>Media</h4>
            
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chatapp;
