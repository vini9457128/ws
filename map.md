# lógica de memorização

    valida quanto vendeu _agora_ em relação a última chamada

    17:30 -> vendeu 10,00(NOW)
    17:35 -> vendeu 15,00(NOW) vendeu  5,00  ultimos  5 minutos
    17:45 -> vendeu 15,00(NOW) vendeu  0,00  ultimos 15 minutos
    18:00 -> vendeu 25,00(NOW) vendeu 10,00  ultimos 30 minutos
    18:00 -> vendeu 35,00(NOW)
    18:05 -> vendeu 40,00(NOW) vendeu  5,00  ultimos  5 minutos

# Google Api

## requerimentos ->

    _google-ads.yaml_ : para configurações da api; arquivo de configuração deve ser setado o _refresh-token_ equivalente ao _customer-id_
    _refresh-token_ : REFRESH TOKEN do cliente que será consultado
    _customer-id_ : ID do cliente que será consultado

## docs ->

    -  Linguagem de consulta (sql): https://developers.google.com/google-ads/api/docs/query/overview?hl=pt-br

## TODO

    [x] - lógica de memorização para google ADS
    [ ] - lógica de memorização para facebook ADS
    [x] - isolar lógicas de memorização em uma classe base
    [x] - ajustar lógica de memorização para ser mais genérica
    [ ] - adicionar método para calcular diferenças de dados entre os periodos salvos em mémoria
    [ ] - ajustar retorno de processos -> 
            {
                "metricas now()": {},
                "memory": {
                    "memory_reference": {},
                    "last_five_minutes": {},
                    "last_fiveteen_minutes": {},
                    "last_thirty_minutes": {},
                }        
            }
            