import pandas as pd

from database.query_database import update_database_sign
from database.query_prod import query_ranking_strategies_M5, query_operations_resume_M5, update_ranking_M5

from base_process.process.expirations.expiration_candle import expiration_operation_M5

class AnalyzeData_Strategies:
    def process_sup_res(dataframe_candles, status_alert):
        
        list_estrategies = list(dataframe_candles["estrategias"].drop_duplicates(keep="last"))
        print(f"*********** list_estrategies: {list_estrategies}")

        dataframe_candles["from"] = pd.to_datetime(dataframe_candles["from"], format="%Y-%m-%d %H:%M:%S")
        print("\n\n\n\n\n *************************** DATAFRAME FROM INFO")
        print(dataframe_candles.info())
        
        try:
            for estrategia in list_estrategies:
                df_analysis_m5  = dataframe_candles[ (dataframe_candles["timeframe"]=="5M") & (dataframe_candles["estrategias"]==estrategia) ]
                list_actives    = list(df_analysis_m5["active_name"].drop_duplicates(keep="last"))

                
                for active in list_actives:
                    print(f"ANALISANDO | {estrategia} -- {active}")
                    df_analysis_m5_active = df_analysis_m5[(df_analysis_m5["active_name"]==active)]

                    list_results_sup_res = []
                    # -----------------------
                    list_results_sup_res_15M = []
                    list_results_sup_res_1H  = []
                    list_results_sup_res_4H = []
                    list_results_sup_res_extrato_tm = []
                    # ----------------------------------
                    list_results_res_15m_extrato_tm = []
                    list_results_sup_15m_extrato_tm = []
                    list_results_res_1h_extrato_tm = []
                    list_results_sup_1h_extrato_tm = []
                    list_results_res_4h_extrato_tm = []
                    list_results_sup_4h_extrato_tm = []

                    for idx_active in df_analysis_m5_active.index:
                        
                        m5_from             = df_analysis_m5_active["from"][idx_active]
                        m5_status_candle    = df_analysis_m5_active["status_candle"][idx_active]
                        m5_active_name      = df_analysis_m5_active["active_name"][idx_active]
                        m5_max              = float(df_analysis_m5_active["max"][idx_active])
                        m5_open             = float(df_analysis_m5_active["open"][idx_active])
                        m5_close            = float(df_analysis_m5_active["close"][idx_active])
                        m5_min              = float(df_analysis_m5_active["min"][idx_active])

                        if len(m5_from) >= 1:

                            df_sup_res = dataframe_candles[ (dataframe_candles["timeframe"]!="5M") &
                                                            (dataframe_candles["estrategias"]==estrategia) &
                                                            (dataframe_candles["active_name"]==m5_active_name)]
                            list_temp_results = []
                            list_results_sup_res_tt_timeframes = []
                            for idx_sup_res in df_sup_res.index:
                                sup_res_timeframe   = df_sup_res["timeframe"][idx_sup_res]
                                sup_res_from        = df_sup_res["from"][idx_sup_res]
                                sup_status_candle   = df_sup_res["status_candle"][idx_sup_res]
                                sup_res_active_name = df_sup_res["active_name"][idx_sup_res]
                                sup_res_min         = float(df_sup_res["min"][idx_sup_res])
                                sup_res_max         = float(df_sup_res["max"][idx_sup_res])
                                if len(sup_res_from) >= 1:
                                    # print(f"\nANALISANDO | M5 --> m5_active_name: {m5_active_name} | m5_min: {m5_min} | m5_max: {m5_max} || {sup_res_timeframe} --> sup_res_active_name: {sup_res_active_name} | sup_res_min: {sup_res_min} | sup_res_max: {sup_res_max}")
                                    valida_timeframe = True
                                    
                                    if sup_res_timeframe == "15M" and m5_from.hour == sup_res_from.hour and m5_from.minute + 15 < sup_res_from.minute:
                                        valida_timeframe = False
                                        print("------------------>>>> NÃO ANALISAR")
                                    elif m5_from <= sup_res_from:
                                        valida_timeframe = False
                                    
                                    if valida_timeframe == True:
                                        if sup_status_candle == "alta":
                                            if m5_status_candle == "alta":
                                                if m5_max >= sup_res_max and m5_close < sup_res_max:
                                                    list_temp_results.append(f"1 - RES - FROM M5: {m5_from} | FROM RES: {sup_res_timeframe} | {sup_res_from}")
                                                    list_results_sup_res_tt_timeframes.append(sup_res_timeframe)
                                                    list_results_sup_res_extrato_tm.append(f"RES - {sup_res_timeframe}")

                                            
                                            elif m5_status_candle == "baixa":
                                                if m5_min >= sup_res_max and m5_open < sup_res_max:
                                                    list_temp_results.append(f"2 - RES - FROM M5: {m5_from} | FROM RES: {sup_res_timeframe} | {sup_res_from}")
                                                    list_results_sup_res_tt_timeframes.append(sup_res_timeframe)
                                                    list_results_sup_res_extrato_tm.append(f"RES - {sup_res_timeframe}")

                                        elif sup_status_candle == "baixa":
                                            if m5_status_candle == "alta":
                                                if m5_min <= sup_res_min and m5_open > sup_res_min:
                                                    list_temp_results.append(f"3 - SUP - FROM M5: {m5_from} | FROM SUP: {sup_res_timeframe} | {sup_res_from}")
                                                    list_results_sup_res_tt_timeframes.append(sup_res_timeframe)
                                                    list_results_sup_res_extrato_tm.append(f"SUP - {sup_res_timeframe}")
                                            
                                            elif m5_status_candle == "baixa":
                                                if m5_min <= sup_res_min and m5_open > sup_res_min:
                                                    list_temp_results.append(f"4 - SUP - FROM M5: {m5_from} | FROM SUP: {sup_res_timeframe} | {sup_res_from}")
                                                    list_results_sup_res_tt_timeframes.append(sup_res_timeframe)
                                                    list_results_sup_res_extrato_tm.append(f"SUP - {sup_res_timeframe}")
                                            
                                        else:
                                            list_temp_results.append("--")
                            list_results_sup_res.append(list_temp_results)
                            list_results_sup_res_15M.append(list_results_sup_res_tt_timeframes.count("15M"))
                            list_results_sup_res_1H.append(list_results_sup_res_tt_timeframes.count("1H"))
                            list_results_sup_res_4H.append(list_results_sup_res_tt_timeframes.count("4H"))
                            # ----------------------------------------------------------------------------------------------------
                            list_results_res_15m_extrato_tm.append(list_results_sup_res_extrato_tm.count("RES - 15M"))
                            list_results_sup_15m_extrato_tm.append(list_results_sup_res_extrato_tm.count("SUP - 15M"))
                            list_results_res_1h_extrato_tm.append(list_results_sup_res_extrato_tm.count("RES - 1H"))
                            list_results_sup_1h_extrato_tm.append(list_results_sup_res_extrato_tm.count("SUP - 1H"))
                            list_results_res_4h_extrato_tm.append(list_results_sup_res_extrato_tm.count("RES - 4H"))
                            list_results_sup_4h_extrato_tm.append(list_results_sup_res_extrato_tm.count("SUP - 4H"))
                            list_results_sup_res_extrato_tm.clear()


                    df_analysis_m5_active["results"]        = list_results_sup_res
                    df_analysis_m5_active["results_15M"]    = list_results_sup_res_15M
                    df_analysis_m5_active["results_1H"]     = list_results_sup_res_1H
                    df_analysis_m5_active["results_4H"]     = list_results_sup_res_4H
                    # --------------------------------------------------------------------------
                    df_analysis_m5_active["res_15m_extrato_tm"] = list_results_res_15m_extrato_tm
                    df_analysis_m5_active["sup_15m_extrato_tm"] = list_results_sup_15m_extrato_tm
                    df_analysis_m5_active["res_1h_extrato_tm"]  = list_results_res_1h_extrato_tm
                    df_analysis_m5_active["sup_1h_extrato_tm"]  = list_results_sup_1h_extrato_tm
                    df_analysis_m5_active["res_4h_extrato_tm"]  = list_results_res_4h_extrato_tm
                    df_analysis_m5_active["sup_4h_extrato_tm"]  = list_results_sup_4h_extrato_tm

                    # df_analysis_m5_active.to_excel(f"{estrategia} - {active}.xlsx")
                    if estrategia == "estrategia_1":
                        try:
                            query_resume = query_operations_resume_M5(active_name=active, estrategia="estrategia_1")
                            update_ranking_M5(obj_results=query_resume[0])
                        except Exception as e:
                            print(f"#### ERRRO PROCESS UPDATE RANK | ERROR: {e} ### ")
                        estrategia_1(estrategia=estrategia, dataframe=df_analysis_m5_active, padrao="PADRAO-M5-V1", version="M5-V1", active=active, status_alert=status_alert)
                    elif estrategia == "estrategia_2":
                        try:
                            query_resume = query_operations_resume_M5(active_name=active, estrategia="estrategia_2")
                            update_ranking_M5(obj_results=query_resume[0])
                        except Exception as e:
                            print(f"#### ERRRO PROCESS UPDATE RANK | ERROR: {e} ### ")
                        estrategia_2(estrategia=estrategia, dataframe=df_analysis_m5_active, padrao="PADRAO-M5-V2", version="M5-V2", active=active, status_alert=status_alert)
                    elif estrategia == "estrategia_3":
                        try:
                            query_resume = query_operations_resume_M5(active_name=active, estrategia="estrategia_3")
                            update_ranking_M5(obj_results=query_resume[0])
                        except Exception as e:
                            print(f"#### ERRRO PROCESS UPDATE RANK | ERROR: {e} ### ")
                        estrategia_3(estrategia=estrategia, dataframe=df_analysis_m5_active, padrao="PADRAO-M5-V3", version="M5-V3", active=active, status_alert=status_alert)
                    elif estrategia == "estrategia_4":
                        try:
                            query_resume = query_operations_resume_M5(active_name=active, estrategia="estrategia_4")
                            update_ranking_M5(obj_results=query_resume[0])
                        except Exception as e:
                            print(f"#### ERRRO PROCESS UPDATE RANK | ERROR: {e} ### ")
                        estrategia_4(estrategia=estrategia, dataframe=df_analysis_m5_active, padrao="PADRAO-M5-V4", version="M5-V4", active=active, status_alert=status_alert)
        except Exception as e:
            print(f"ERROR DF: {e}")




def prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h):
    
    dataframe["from"] = dataframe["from"].dt.strftime('%Y-%m-%d %H:%M:%S')
    max_idx = max(list(dataframe.index))
    expiration = expiration_operation_M5(dataframe["from"][max_idx])
    mercado = "-"
    if "OTC" in active:
        mercado = "otc"
    else:
        mercado = "aberto"

    obj_to_database = {
        "open_time": expiration["open_time"],
        "alert_datetime": expiration["alert_datetime"],
        "expiration_alert": expiration["expiration_alert"],
        "expiration_alert_timestamp": expiration["expiration_alert_timestamp"],
        "alert_time_update": expiration["alert_time_update"],
        "resultado": expiration["resultado"],
        "status_alert": status_alert,
        "padrao": padrao,
        "version": version,
        "name_strategy": f"{active}-{version}",
        "direction": direction,
        "active": active,
        "mercado": mercado,
        "observation": observation,
        "result_confluencias": result_confluencias,
        "sup_m15": sup_m15,
        "sup_1h": sup_1h,
        "sup_4h": sup_4h,
        "res_m15": res_m15,
        "res_1h": res_1h,
        "res_4h": res_4h,
    }
    if direction == "call" or direction == "put":
        update_database_sign(obj_sign=obj_to_database)
    if result_confluencias == True:
        print(f"\n ------------------------------ Enviar sinal ao banco de dados: SIM | RESULT-CONFLUÊNCIAS: {result_confluencias} ------------------------------ ")
    else:
        print(f"\n ------------------------------ Enviar sinal ao banco de dados: NÃO | RESULT-CONFLUÊNCIAS: {result_confluencias} ------------------------------ ")
    print(f"SIGNAL TO DATABASE ------------------->>>>> {obj_to_database}\n\n")

# ----------------------------------------------------------------------
def estrategia_1(estrategia, dataframe, status_alert, padrao, version, active):
    list_idx = list(range(0, len(dataframe.index)))
    dataframe.index = list_idx
    print(f"-------------------------------------------------------> estratégia: {estrategia}")
    print(dataframe[["from", "active_name", "status_candle"]]) #, "res_15m_extrato_tm", "sup_15m_extrato_tm", "res_1h_extrato_tm", "sup_1h_extrato_tm", "res_4h_extrato_tm", "sup_4h_extrato_tm"]])
    
    result_confluencias = False
    current_id = max(list_idx)
    id_5 = current_id -4
    id_4 = current_id -3
    id_3 = current_id -2
    id_2 = current_id -1
    id_1 = current_id
    
    direction = "-"
    observation = "-"

  
    sup_m15  = dataframe["sup_15m_extrato_tm"][id_1]
    sup_1h   = dataframe["sup_1h_extrato_tm"][id_1]
    sup_4h   = dataframe["sup_4h_extrato_tm"][id_1]
    res_m15  = dataframe["res_15m_extrato_tm"][id_1]
    res_1h  = dataframe["res_1h_extrato_tm"][id_1]
    res_4h  = dataframe["res_4h_extrato_tm"][id_1]
    # if dataframe["status_candle"][id_5] == "baixa" and dataframe["status_candle"][id_4] == "alta" and dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
    if dataframe["status_candle"][id_5] == "baixa" and dataframe["status_candle"][id_4] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
        if dataframe["sup_15m_extrato_tm"][id_1] >= 2 or dataframe["sup_1h_extrato_tm"][id_1] >= 1 or  dataframe["sup_4h_extrato_tm"][id_1] >= 1:
            direction = "call"
            result_confluencias = True
        else:
            observation = "call - sem conf. sup res"
    
    # elif dataframe["status_candle"][id_5] == "alta" and dataframe["status_candle"][id_4] == "baixa" and dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
    elif dataframe["status_candle"][id_5] == "alta" and dataframe["status_candle"][id_4] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
        if dataframe["res_15m_extrato_tm"][id_1] >= 3 or dataframe["res_1h_extrato_tm"][id_1] >= 1 or  dataframe["res_4h_extrato_tm"][id_1] >= 1:
            direction = "put"
            result_confluencias = True
        else:
            observation = "put - sem conf. sup res"
    
    prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h)

# -----------------------------------------------------------------------
def estrategia_2(estrategia, dataframe, status_alert, padrao, version, active):
    list_idx = list(range(0, len(dataframe.index)))
    dataframe.index = list_idx
    print(f"-------------------------------------------------------> estratégia: {estrategia}")
    print(dataframe[["from", "active_name", "status_candle"]])
    
    result_confluencias = False
    direction = "-"
    observation = "-"
    current_id = max(list_idx)
    id_7 = current_id -6
    id_6 = current_id -5
    id_5 = current_id -4
    id_4 = current_id -3
    id_3 = current_id -2
    id_2 = current_id -1
    id_1 = current_id -0

    sup_m15  = dataframe["sup_15m_extrato_tm"][id_1]
    sup_1h   = dataframe["sup_1h_extrato_tm"][id_1]
    sup_4h   = dataframe["sup_4h_extrato_tm"][id_1]
    res_m15  = dataframe["res_15m_extrato_tm"][id_1]
    res_1h  = dataframe["res_1h_extrato_tm"][id_1]
    res_4h  = dataframe["res_4h_extrato_tm"][id_1]
    if dataframe["status_candle"][id_7] == "baixa" and dataframe["status_candle"][id_6] == "alta" and dataframe["status_candle"][id_5] == "baixa" and dataframe["status_candle"][id_4] == "baixa" and dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "baixa":
        if dataframe["sup_15m_extrato_tm"][id_1] == 1 or dataframe["sup_1h_extrato_tm"][id_1] == 1 or  dataframe["sup_4h_extrato_tm"][id_1] == 1:
            direction = "call"
            result_confluencias = True
        else:
            observation = "call - sem conf. sup res"

    elif dataframe["status_candle"][id_7] == "alta" and dataframe["status_candle"][id_6] == "baixa" and dataframe["status_candle"][id_5] == "alta" and dataframe["status_candle"][id_4] == "alta" and dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "alta":
        if dataframe["res_15m_extrato_tm"][id_1] == 1 or dataframe["res_1h_extrato_tm"][id_1] == 1 or  dataframe["res_4h_extrato_tm"][id_1] == 1:
            direction = "put"
            result_confluencias = True
        else:
            observation = "put - sem conf. sup res"
    
    prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h)

# ----------------------------------------------------------------------
def estrategia_3(estrategia, dataframe, status_alert, padrao, version, active):
    list_idx = list(range(0, len(dataframe.index)))
    dataframe.index = list_idx
    print(f"-------------------------------------------------------> estratégia: {estrategia}")
    print(dataframe[["from", "active_name", "status_candle"]])
    
    confluencia_1 = "no"
    confluencia_2 = "no"
    confluencia_3 = "no"
    result_confluencias = False
    observation = "-"
    direction = "-"
    observation_2 = "#"
    sup_m15 = None
    sup_1h = None
    sup_4h = None
    res_m15 = None
    res_1h = None
    res_4h = None
    for current_id in dataframe.index:
        if current_id == 2:
            id_3 = current_id -2
            id_2 = current_id -1
            id_1 = current_id -0
            if dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
                confluencia_1 = "yes"

            elif dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
                confluencia_1 = "yes"
        # ----------------------------
        elif current_id == 5:
            id_3 = current_id -2
            id_2 = current_id -1
            id_1 = current_id -0
            if dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
                confluencia_2 = "yes"

            elif dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
                confluencia_2 = "yes"
        # ----------------------------
        elif current_id == 8:
            id_3 = current_id -2
            id_2 = current_id -1
            id_1 = current_id -0
            if dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
                confluencia_3 = "yes"

            elif dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
                confluencia_3 = "yes"
        # ----------------------------
        elif current_id == 11:
            id_3 = current_id -2
            id_2 = current_id -1
            id_1 = current_id -0
            sup_m15  = dataframe["sup_15m_extrato_tm"][id_1]
            sup_1h   = dataframe["sup_1h_extrato_tm"][id_1]
            sup_4h   = dataframe["sup_4h_extrato_tm"][id_1]
            res_m15  = dataframe["res_15m_extrato_tm"][id_1]
            res_1h  = dataframe["res_1h_extrato_tm"][id_1]
            res_4h  = dataframe["res_4h_extrato_tm"][id_1]
            if dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
                if dataframe["res_15m_extrato_tm"][id_1] >= 2 or dataframe["res_1h_extrato_tm"][id_1] >= 1 or  dataframe["res_4h_extrato_tm"][id_1] >= 1:
                    direction = "put"
                else:
                    observation_2 = "put - sem conf. sup res"

            elif dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
                if dataframe["sup_15m_extrato_tm"][id_1] >= 2 or dataframe["sup_1h_extrato_tm"][id_1] >= 1 or  dataframe["sup_4h_extrato_tm"][id_1] >= 1:
                    direction = "call"
                else:
                    observation_2 = "call - sem conf. sup res"
    
    observation = f"Q1: {confluencia_1} - Q2: {confluencia_2} - Q3: {confluencia_3} - {observation_2}"
    if confluencia_1 == "no" and confluencia_2 == "no" and confluencia_3 == "no":
        if direction == "put" or direction == "call":
            result_confluencias = True
    else:
        if "call" in direction:
            direction = "operation-canceled-call"
        elif "put" in direction:
            direction = "operation-canceled-put"
        else:
            direction = "-"
    
    print(f"\n\n -----> CONFLUÊNCIAS {active} | RESULTADO: {result_confluencias} | OBS: {observation}")
    
    prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h)

# ----------------------------------------------------------------------
def estrategia_4(estrategia, dataframe, status_alert, padrao, version, active):
    list_idx = list(range(0, len(dataframe.index)))
    dataframe.index = list_idx
    print(f"-------------------------------------------------------> estratégia: {estrategia}")
    print(dataframe[["from", "active_name", "status_candle"]])
    
    result_confluencias = False
    current_id = max(list_idx)
    id_7 = current_id -6
    id_6 = current_id -5
    id_5 = current_id -4
    # id_4 = current_id -3
    id_3 = current_id -2
    # id_2 = current_id -1
    id_1 = current_id -0
    
    direction = "-"
    observation = "-"
    sup_m15  = dataframe["sup_15m_extrato_tm"][id_1]
    sup_1h   = dataframe["sup_1h_extrato_tm"][id_1]
    sup_4h   = dataframe["sup_4h_extrato_tm"][id_1]
    res_m15  = dataframe["res_15m_extrato_tm"][id_1]
    res_1h  = dataframe["res_1h_extrato_tm"][id_1]
    res_4h  = dataframe["res_4h_extrato_tm"][id_1]
    if dataframe["status_candle"][id_7] == "baixa" and dataframe["status_candle"][id_6] == "alta" and dataframe["status_candle"][id_5] == "alta" and dataframe["status_candle"][id_3] == "baixa":
        if dataframe["res_15m_extrato_tm"][id_1] >= 2 or dataframe["res_1h_extrato_tm"][id_1] >= 1 ==  dataframe["res_4h_extrato_tm"][id_1] >= 1:
            direction = "put"
            result_confluencias = True
        else:
            observation = "put - sem conf. sup res"

    elif dataframe["status_candle"][id_7] == "alta" and dataframe["status_candle"][id_6] == "baixa" and dataframe["status_candle"][id_5] == "baixa" and dataframe["status_candle"][id_3] == "alta":
        if dataframe["sup_15m_extrato_tm"][id_1] >= 2 or dataframe["sup_1h_extrato_tm"][id_1] == 0 or  dataframe["sup_4h_extrato_tm"][id_1] >= 1:
            direction = "call"
            result_confluencias = True
        else:
            observation = "call - sem conf. sup res"
    
    prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h)