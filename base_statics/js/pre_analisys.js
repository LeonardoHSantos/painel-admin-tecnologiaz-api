console.log("pre_analysis.js carregado...");

function createPreAnalysis(url){
    console.log(url);
    let body = {
        "valida_email": [true, "leonardotradeiq@gmail.com"],
        "valida_password": [true, "ContaTesteTrade"],
        "valida_datas": [true, "2023-05-08", "2023-05-08"],
        "valida_input_estrategia": [true, "estrategia_3"],
        "valida_input_paridade": [true, "EURJPY"],
        "valida_input_sup_res_15m": [true, "1"],
        "valida_input_sup_res_1h": ["ignore"],
        "valida_input_sup_res_4h": ["ignore"]
    }
    let headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "text/plain"
    }

    fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(body)
    }).then((data)=>{
        console.log(data);
        return data.json();
    }).then((data)=>{
        console.log(data);
    })
}