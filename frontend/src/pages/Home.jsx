import { Component, useEffect, useState } from "react";

function Home() {
  return (
    <div className="w-full justify-center items-center">
      <div className="w-full flexbox items-center py-6">
        <h1 className="text-4xl text-center">Student</h1>
      </div>
      <div className="w-full flexbox items-center px-20 py-12 mx-15">
        <Table />
      </div>
    </div>
  );
}

function Table(){
  const [data, setData] = useState([])
  useEffect(() => {
    fetch("http://127.0.0.1:5000/current_attendance", {
      method: "GET",
      //headers: {},
    }).then((raw) => {
        console.log(raw);
        return raw.json()
      }).then((value) => {
        console.log(value["data"]);
        setData(value["data"]);
        console.log(value);
      }
    ),
    []
  }, []);
  //const data = [{firstname:"bob", lastname:"smith", present:true}]
  return (
    <div className="text-xl">
      <table className="w-full m-0 border">
        <tr className="w-full border p-2">
          <th className="w-1/6 px-5 text-left font-semibold">First Name</th>
          <th className="w-1/6 px-1 text-left font-semibold">Last Name</th>
          <th className="w-1/2 px-1 text-left font-semibold">Details</th>
          <th className="w-1/6 text-right px-5 font-semibold">Here</th>
        </tr>
        {data.map((val, key) => {
          return (
            <tr key={key} className="w-full p-1">
              <td className="w-1/6 px-5">{val.firstname}</td>
              <td className="w-1/6 px-1">{val.lastname}</td>
              <td className="w-1/2 px-1">{val.details}</td>
              <td className="w-1/6 text-right px-5">{
                val.present ? '✅' : '❌'
              }</td>
            </tr>
          )
        })}
      </table>
    </div>
  );
}
export default Home;
