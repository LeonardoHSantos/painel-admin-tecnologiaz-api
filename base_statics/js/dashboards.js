
var dash_1;
function createDashboardResults(element_id, element_canvas, list_hours, list_results_win, list_results_loss){
    // const ctx = document.getElementById('myChart');
    const ctx = document.getElementById(element_id);
    try {
        element_canvas.destroy();
    } catch (error) {}

    let data = {
        datasets: [{
            type: 'bar',
            label: 'win',
            data: list_results_win,
            backgroundColor: '#00ff0d',
        }, {
            type: 'bar',
            label: 'loss',
            data: list_results_loss,
            backgroundColor: '#ff0000',
        }],
        labels: list_hours
    }
    // ------------------------------
    element_canvas = new Chart(ctx, {
        // type: 'bar',
        data: data,
        options: {
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true,
                }
            },
        },
    });
}

function prepareDataToDashboard(){
    let list_hours = [0, 1, 2, 3, 4, 5];
    const PromisseA = new Promise((resolve, reject)=>{
        let obj_results = [
            {"hora": 9, "result": "loss"},
            {"hora": 9, "result": "loss"},
            {"hora": 9, "result": "win"},
            {"hora": 9, "result": "win"},

            {"hora": 0, "result": "win"},
            {"hora": 0, "result": "win"},
            {"hora": 1, "result": "loss"},
            {"hora": 1, "result": "win"},
            {"hora": 1, "result": "win"},
            {"hora": 1, "result": "win"},
            {"hora": 1, "result": "win"},
            {"hora": 1, "result": "win"},
            {"hora": 2, "result": "loss"},
            {"hora": 2, "result": "winn"},
            {"hora": 2, "result": "loss"},
            {"hora": 2, "result": "loss"},
            {"hora": 2, "result": "win"},
            {"hora": 2, "result": "loss"},
            {"hora": 3, "result": "win"},
            {"hora": 3, "result": "win"},
            {"hora": 7, "result": "loss"},
            {"hora": 7, "result": "win"},
            {"hora": 7, "result": "win"},
            {"hora": 7, "result": "win"},
        ];
        let lista_horarios = [];
        for (i=0; i < obj_results.length; i++){
            console.log(obj_results[i]["hora"], obj_results[i]["result"])
            if (!lista_horarios.includes(obj_results[i]["hora"])){
                lista_horarios.push(obj_results[i]["hora"]);
            }
        }
        console.log("valores sort ", numbers);
        resolve(lista_horarios)
    }).then((lista_horarios)=>{
        console.log(lista_horarios)
        let list_results_win = [12, 3, 20, 11, 23, 9];
        let list_results_loss = [23, 12, 9, 11, 19, 12]
    
    
        createDashboardResults(
            "myChart",
            dash_1,
            lista_horarios,
            list_results_win,
            list_results_loss
        )
    })


}
prepareDataToDashboard();