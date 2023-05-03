console.log("scriptDashboard.js carregado...");

function getDataDashboardPrincipal(url) {
    console.log("getDataDashboardPrincipal acionado...");

    let input_data_inicial = document.getElementById("input-data-inicial").value;
    let input_data_final = document.getElementById("input-data-final").value;
    let input_mercado = document.getElementById("input-mercado").value;
    let input_ativo = document.getElementById("input-ativo").value;
    let input_direcao = document.getElementById("input-direcao").value;
    let input_resultado = document.getElementById("input-resultado").value;
    let input_estrategia = document.getElementById("input-estrategia").value;
    let input_alerta = document.getElementById("input-alerta").value;
    let data = {
        "data_inicio": input_data_inicial,
        "data_fim": input_data_final,
        "mercado": input_mercado,
        "active": input_ativo,
        "direction": input_direcao,
        "resultado": input_resultado,
        "padrao": input_estrategia,
        "status_alert": input_alerta
    }
    console.log(data);

    fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
    }).then((data)=>{
        return data.json();
    }).then((data)=> {
        let data_results = JSON.parse(data["data"]);
        document.querySelector(".table-results-resume tbody").remove()
        document.querySelector(".table-results-resume").innerHTML += `<tbody></tbody>`;
        let table_results = document.querySelector(".table-results-resume tbody");
        for (let data_idx in data_results) {
            table_results.innerHTML += `
                <tr>
                    <td class="result-comum">${data_idx}</td>
                    <td class="result-comum">${data_results[data_idx]["expiration_alert"]}</td>
                    <td class="result-comum">${data_results[data_idx]["padrao"]}</td>
                    <td class="result-comum">${data_results[data_idx]["status_alert"]}</td>
                    <td class="result-comum">${data_results[data_idx]["mercado"]}</td>
                    <td class="result-comum">${data_results[data_idx]["active"]}</td>
                    <td class="${data_results[data_idx]["className_direction"]}">${data_results[data_idx]["direction"]}</td>
                    <td class="${data_results[data_idx]["class_name"]}">${data_results[data_idx]["resultado"]}</td>

                    <td class="result-comum">${data_results[data_idx]["sup_m15"]}</td>
                    <td class="result-comum">${data_results[data_idx]["sup_1h"]}</td>
                    <td class="result-comum">${data_results[data_idx]["sup_4h"]}</td>
                    <td class="result-comum">${data_results[data_idx]["res_m15"]}</td>
                    <td class="result-comum">${data_results[data_idx]["res_1h"]}</td>
                    <td class="result-comum">${data_results[data_idx]["res_4h"]}</td>
                </tr>
            `;

        }
    })
}