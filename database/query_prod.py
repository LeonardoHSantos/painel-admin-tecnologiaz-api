from database.conn import conn_db_producao
from base_process.process.expirations.expiration_candle import datetime_now, convert_datetime_to_string
from config_auth import TABLE_NAME_OPERATIONS

# def query_database_prod_estrategia(data_inicio, data_fim):
def query_database_prod_estrategia(string_query):
    try:
        conn = conn_db_producao()
        cursor = None
        dict_results = dict()
        resume_results = None
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            comando_query = f'''
                SELECT
                    id, mercado, active, padrao, direction, resultado, status_alert,
                    alert_datetime, expiration_alert, alert_time_update,
                    name_strategy,
                    sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h
                 from
                    {TABLE_NAME_OPERATIONS}
                {string_query}
                '''
            # WHERE
            #         expiration_alert >= "{data_inicio}" and expiration_alert <= "{data_fim}"
            print(comando_query)
            cursor.execute(comando_query)
            result_query    = cursor.fetchall()
            tt_query = len(result_query)
            print("\n\n----------------------- PROD | result query ")
            # print(result_query)
            print(f"TT QUERY PROD: {tt_query}")
            print("FIM PROD -----------------------")
            tt_call = 0
            tt_put = 0
            list_results = []
            tt_win_call = 0
            tt_loss_call = 0
            tt_win_put = 0
            tt_loss_put = 0

            if tt_query >= 1:
                for registro in result_query:
                    _id                 = registro[0]
                    _mercado            = registro[1]
                    _active             = registro[2]
                    _padrao             = registro[3]
                    _direction          = registro[4]
                    _resultado          = registro[5]
                    _status_alert       = registro[6]
                    _alert_datetime     = registro[7]
                    _expiration_alert   = registro[8]
                    _alert_time_update  = registro[9]
                    _name_strategy      = registro[10]
                    # --------------------------------
                    _sup_m15            = registro[11]
                    _sup_1h             = registro[12]
                    _sup_4h             = registro[13]
                    _res_m15            = registro[14]
                    _res_1h             = registro[15]
                    _res_4h             = registro[16]

                    _result_temp = None
                    className = "result-empate"
                    if _resultado == "win":
                        _result_temp = "win"
                        className = "result-win"
                    # ------------------------------
                    elif _resultado == "loss":
                        _result_temp = "loss"
                        className = "result-loss"
                   
                    className_direction = "direction-comum"
                    if _direction == "call":
                        tt_call = tt_call + 1
                        className_direction = "direction-call"
                        if _result_temp == "win":
                            tt_win_call = tt_win_call + 1
                        elif _result_temp == "loss":
                            tt_loss_call = tt_loss_call + 1
                    # -----------------------------------------
                    elif _direction == "put":
                        tt_put = tt_put + 1
                        className_direction = "direction-put"
                        if _result_temp == "win":
                            tt_win_put = tt_win_put + 1
                        elif _result_temp == "loss":
                            tt_loss_put = tt_loss_put + 1
                    
                    
                        
                    
                    data = {
                        f"{_id}": {
                            "id": _id,
                            "mercado": _mercado,
                            "active": _active,
                            "padrao": _padrao,
                            "direction": _direction,
                            "resultado": _resultado,
                            "expiration_alert": convert_datetime_to_string(_expiration_alert),
                            "status_alert": _status_alert,
                            "class_name": className,
                            "className_direction": className_direction,
                            "sup_m15": _sup_m15,
                            "sup_1h": _sup_1h,
                            "sup_4h": _sup_4h,
                            "res_m15": _res_m15,
                            "res_1h": _res_1h,
                            "res_4h": _res_4h,
                            "alert_datetime": convert_datetime_to_string(_alert_datetime),
                            "alert_time_update": convert_datetime_to_string(_alert_time_update),
                        }
                    }
                    # print(data)
                    dict_results.update(data)
                resume_results = {
                    "tt_query": int(tt_query),
                    "tt_call": tt_call,
                    "tt_put": tt_put,
                    "tt_win": tt_win_call + tt_win_put,
                    "tt_loss": tt_loss_call + tt_loss_put,

                    "tt_win_call": tt_win_call,
                    "tt_loss_call": tt_loss_call,

                    "tt_win_put": tt_win_put,
                    "tt_loss_put": tt_loss_put,
                }
                
                    # print(f"_id: {_id} | _mercado: {_mercado} | _active: {_active} | _padrao: {_padrao} | _direction: {_direction} | _resultado: {_resultado} | _expiration_alert: {_expiration_alert}")
        try:
            cursor.close()
            conn["conn"].close()
            print(" DB - DESCONECTADO ")
        except Exception as e:
            print(f"ERROR QUERY 1 | ERROR: {e}")
        return dict_results, resume_results
    except Exception as e:
        print(f"ERROR QUERY 2 | ERROR: {e}")